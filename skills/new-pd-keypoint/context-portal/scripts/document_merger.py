"""
文档合并器

智能合并变更内容到基础文档的正确位置
"""

import re
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Tuple
from enum import Enum

from document_parser import DocumentParser, DocumentStructure, Heading, find_module_path
from content_extractor import ContentExtractor, ExtractedContent, ContentType, analyze_change_intent


class MergeStrategy(Enum):
    """合并策略"""
    APPEND = "append"  # 追加到末尾
    INSERT_UNDER = "insert_under"  # 插入到指定标题下
    REPLACE_SECTION = "replace_section"  # 替换整个章节
    MERGE_TABLES = "merge_tables"  # 合并表格


@dataclass
class MergePlan:
    """合并计划"""
    strategy: MergeStrategy
    target_path: List[str]  # 目标路径
    insert_after: Optional[str] = None  # 插入到哪个标题之后
    new_content: str = ""
    reason: str = ""
    parent_level: int = 0  # 父标题级别


@dataclass
class MergeResult:
    """合并结果"""
    success: bool
    content: str = ""
    message: str = ""
    applied_plans: List[MergePlan] = field(default_factory=list)


class DocumentMerger:
    """文档合并器"""
    
    # 模块关键词映射表
    MODULE_KEYWORDS = {
        '泳道新建': ['泳道新建', '创建泳道', '泳道环境申请'],
        '泳道变更': ['泳道变更', '修改泳道'],
        '泳道注销': ['泳道注销', '销毁泳道'],
        '工单字段': ['工单字段', '字段定义', '字段整理', '字段'],
        '业务规则': ['业务规则', '规则'],
        '状态定义': ['状态定义', '状态'],
        '工单中心': ['工单中心', '工单'],
        '泳道': ['泳道'],
    }
    
    def __init__(self):
        self.parser = DocumentParser()
        self.extractor = ContentExtractor()
    
    def merge(self, base_content: str, change_content: str) -> MergeResult:
        """
        将变更内容合并到基础文档
        
        Args:
            base_content: 基础文档内容
            change_content: 变更文档内容
            
        Returns:
            MergeResult 合并结果
        """
        # 解析基础文档
        base_structure = self.parser.parse(base_content)
        
        # 提取变更内容
        extracted = self.extractor.extract(change_content)
        
        # 分析变更意图
        intent = analyze_change_intent(change_content)
        
        # 制定合并计划
        plan = self._create_merge_plan(base_structure, extracted, intent)
        
        # 执行合并
        return self._execute_merge(base_content, base_structure, extracted, plan)
    
    def _create_merge_plan(self, base_structure: DocumentStructure,
                          extracted: ExtractedContent,
                          intent: Dict[str, Any]) -> MergePlan:
        """
        创建合并计划
        
        Args:
            base_structure: 基础文档结构
            extracted: 提取的变更内容
            intent: 变更意图
            
        Returns:
            MergePlan 合并计划
        """
        # 1. 确定目标模块 - 首先尝试从变更文档提取
        target_module = extracted.target_module or intent.get('target_module')
        target_section = extracted.target_section or intent.get('target_section')
        
        # 2. 从变更文档标题中进一步提取目标信息
        headings = extracted.get_headings()
        for h in headings:
            title = h.title
            # 检测泳道相关
            if '泳道' in title:
                if '新建' in title or '创建' in title:
                    target_module = '泳道新建'
                elif '变更' in title:
                    target_module = '泳道变更'
                else:
                    target_module = '泳道'
            # 检测字段相关
            if '字段' in title:
                target_section = '工单字段'
        
        # 3. 查找模块路径
        module_path = None
        parent_level = 0
        if target_module:
            module_keywords = self.MODULE_KEYWORDS.get(target_module, [target_module])
            module_path = find_module_path(base_structure, module_keywords)
        
        # 4. 如果没有找到模块，尝试使用默认路径
        if not module_path:
            # 尝试工单中心路径
            module_path = find_module_path(base_structure, ['工单中心'])
        
        if not module_path:
            # 最后的回退：追加到文档末尾
            return MergePlan(
                strategy=MergeStrategy.APPEND,
                target_path=[],
                new_content=self._format_content(extracted, parent_level=1),
                reason="未找到合适位置，追加到文档末尾",
                parent_level=1
            )
        
        # 5. 获取父标题级别
        parent_heading = base_structure.find_path(module_path)
        if parent_heading:
            parent_level = parent_heading.level
        
        # 6. 查找目标章节
        if target_section:
            section_keywords = self.MODULE_KEYWORDS.get(target_section, [target_section])
            
            # 尝试在找到的模块路径下查找目标章节
            if parent_heading:
                for keyword in section_keywords:
                    for child in parent_heading.children:
                        if keyword in child.text:
                            # 找到目标章节，在其下插入
                            full_path = module_path + [child.text]
                            return MergePlan(
                                strategy=MergeStrategy.INSERT_UNDER,
                                target_path=full_path,
                                new_content=self._format_content(extracted, parent_level=child.level),
                                reason=f"找到目标章节 {child.text}，在其下插入内容",
                                parent_level=child.level
                            )
        
        # 7. 在模块下创建新章节
        if parent_heading:
            return MergePlan(
                strategy=MergeStrategy.INSERT_UNDER,
                target_path=module_path,
                new_content=self._format_content(extracted, parent_level=parent_level, add_heading=True),
                reason=f"在模块 {module_path[-1]} 下创建新章节",
                parent_level=parent_level
            )
        
        # 8. 最后的回退
        return MergePlan(
            strategy=MergeStrategy.APPEND,
            target_path=[],
            new_content=self._format_content(extracted, parent_level=1, add_heading=True),
            reason="未找到合适位置，追加到文档末尾",
            parent_level=1
        )
    
    def _format_content(self, extracted: ExtractedContent, 
                       parent_level: int = 1,
                       add_heading: bool = False) -> str:
        """
        格式化提取的内容为Markdown
        
        Args:
            extracted: 提取的内容
            parent_level: 父标题级别
            add_heading: 是否添加标题（当目标章节不存在时使用）
            
        Returns:
            格式化后的Markdown文本
        """
        lines = []
        
        # 确定内容的基础级别（作为父标题的子内容）
        content_base_level = min(parent_level + 1, 6)
        
        # 只在需要时添加章节标题（当目标章节不存在时）
        if add_heading and extracted.target_section:
            hashes = '#' * content_base_level
            lines.append(f"\n{hashes} {extracted.target_section}")
        
        # 添加各内容块
        first_heading = True
        for block in extracted.blocks:
            if block.type == ContentType.HEADING:
                # 跳过文档主标题，如果已经添加了章节标题
                if first_heading and block.level == 1 and add_heading:
                    first_heading = False
                    continue
                first_heading = False
                
                # 调整标题级别，使其成为父标题的子内容
                # 保持相对层级关系，但基于父级别调整
                relative_level = max(1, block.level)
                adjusted_level = min(parent_level + relative_level, 6)
                hashes = '#' * adjusted_level
                lines.append(f"{hashes} {block.title}")
            elif block.type == ContentType.PARAGRAPH:
                # 过滤掉说明性段落
                if not self._is_fluff_text(block.raw_content):
                    lines.append(block.raw_content)
            else:
                lines.append(block.raw_content)
            lines.append('')  # 空行分隔
        
        return '\n'.join(lines)
    
    def _is_fluff_text(self, text: str) -> bool:
        """判断是否为无关的说明性文本"""
        fluff_patterns = [
            r'^根据实际工单数据',
            r'^本文档用于',
            r'^注[：:]',
            r'^注意[：:]',
        ]
        for pattern in fluff_patterns:
            if re.search(pattern, text.strip()):
                return True
        return False
    
    def _execute_merge(self, base_content: str,
                      base_structure: DocumentStructure,
                      extracted: ExtractedContent,
                      plan: MergePlan) -> MergeResult:
        """
        执行合并计划
        
        Args:
            base_content: 基础文档内容
            base_structure: 基础文档结构
            extracted: 提取的变更内容
            plan: 合并计划
            
        Returns:
            MergeResult 合并结果
        """
        lines = base_content.split('\n')
        
        if plan.strategy == MergeStrategy.APPEND:
            # 追加到末尾
            new_content = base_content.rstrip() + '\n\n' + plan.new_content
            
        elif plan.strategy == MergeStrategy.INSERT_UNDER:
            # 插入到指定路径下
            target_heading = base_structure.find_path(plan.target_path)
            
            if target_heading:
                # 找到插入位置
                insert_line = self._find_insert_position(
                    base_structure, target_heading, extracted
                )
                
                # 插入新内容
                new_lines = lines[:insert_line] + \
                           plan.new_content.split('\n') + \
                           lines[insert_line:]
                new_content = '\n'.join(new_lines)
            else:
                # 未找到目标，回退到追加
                new_content = base_content.rstrip() + '\n\n' + plan.new_content
                plan.reason += "（目标未找到，回退到追加）"
        else:
            new_content = base_content.rstrip() + '\n\n' + plan.new_content
        
        return MergeResult(
            success=True,
            content=new_content,
            message=f"合并成功: {plan.reason}",
            applied_plans=[plan]
        )
    
    def _find_insert_position(self, structure: DocumentStructure,
                             parent_heading: Heading,
                             extracted: ExtractedContent) -> int:
        """
        找到在父标题下插入新内容的最佳位置
        
        Args:
            structure: 文档结构
            parent_heading: 父标题
            extracted: 提取的变更内容
            
        Returns:
            插入行号
        """
        # 获取父标题的内容范围
        parent_start = parent_heading.line_number
        
        if parent_heading.children:
            # 有子标题，找到最后一个子标题的结束位置
            last_child = parent_heading.children[-1]
            return self._get_heading_end_line(structure, last_child)
        else:
            # 没有子标题，返回父标题内容结束位置
            # 查找下一个同级标题
            for i in range(parent_start + 1, len(structure.raw_lines)):
                line = structure.raw_lines[i]
                match = re.match(r'^(#{1,6})\s+', line)
                if match:
                    level = len(match.group(1))
                    if level <= parent_heading.level:
                        return i
            return len(structure.raw_lines)
    
    def _get_heading_end_line(self, structure: DocumentStructure,
                             heading: Heading) -> int:
        """获取标题内容的结束行号"""
        if heading.children:
            last_child = heading.children[-1]
            return self._get_heading_end_line(structure, last_child)
        
        # 查找下一个同级或更高级标题
        for i in range(heading.line_number + 1, len(structure.raw_lines)):
            line = structure.raw_lines[i]
            match = re.match(r'^(#{1,6})\s+', line)
            if match:
                level = len(match.group(1))
                if level <= heading.level:
                    return i
        return len(structure.raw_lines)


def merge_documents(base_content: str, change_content: str) -> str:
    """
    合并文档的便捷函数
    
    Args:
        base_content: 基础文档内容
        change_content: 变更文档内容
        
    Returns:
        合并后的文档内容
    """
    merger = DocumentMerger()
    result = merger.merge(base_content, change_content)
    
    if result.success:
        return result.content
    else:
        raise Exception(f"合并失败: {result.message}")


if __name__ == '__main__':
    # 测试
    base = """# 产品上下文

## 工单中心

### 泳道新建

#### 功能描述

已有功能描述
"""
    
    change = """# 泳道新建字段

## 工单字段

| 字段 | 说明 |
|------|------|
| 名称 | 名称说明 |
"""
    
    merger = DocumentMerger()
    result = merger.merge(base, change)
    print(f"成功: {result.success}")
    print(f"消息: {result.message}")
    print(f"策略: {result.applied_plans[0].strategy}")
    print("\n合并结果：")
    print(result.content)
