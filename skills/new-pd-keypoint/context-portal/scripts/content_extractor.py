"""
内容提取器

从变更文档中提取结构化内容，识别内容类型和目标位置
"""

import re
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum


class ContentType(Enum):
    """内容类型枚举"""
    HEADING = "heading"
    TABLE = "table"
    PARAGRAPH = "paragraph"
    LIST = "list"
    CODE_BLOCK = "code_block"
    UNKNOWN = "unknown"


@dataclass
class ContentBlock:
    """内容块"""
    type: ContentType
    raw_content: str
    level: int = 0  # 标题级别（仅标题类型）
    title: str = ""  # 标题文本（仅标题类型）
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __repr__(self):
        if self.type == ContentType.HEADING:
            return f"ContentBlock(HEADING: {self.title})"
        return f"ContentBlock({self.type.value})"


@dataclass
class ExtractedContent:
    """提取的内容集合"""
    title: str = ""
    blocks: List[ContentBlock] = field(default_factory=list)
    target_module: Optional[str] = None  # 目标模块名称
    target_section: Optional[str] = None  # 目标章节
    
    def get_headings(self) -> List[ContentBlock]:
        """获取所有标题块"""
        return [b for b in self.blocks if b.type == ContentType.HEADING]
    
    def get_tables(self) -> List[ContentBlock]:
        """获取所有表格块"""
        return [b for b in self.blocks if b.type == ContentType.TABLE]


class ContentExtractor:
    """内容提取器"""
    
    def __init__(self):
        self.heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$')
        self.table_sep_pattern = re.compile(r'^\|[-:\s|]+\|$')
        self.list_pattern = re.compile(r'^(\s*)([-*+]|\d+\.)\s+(.+)$')
        self.code_block_pattern = re.compile(r'^```(\w*)$')
    
    def extract(self, content: str) -> ExtractedContent:
        """
        从变更文档中提取结构化内容
        
        Args:
            content: Markdown文本
            
        Returns:
            ExtractedContent 提取的内容
        """
        lines = content.split('\n')
        result = ExtractedContent()
        
        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            # 跳过空行
            if not stripped:
                i += 1
                continue
            
            # 检测标题
            heading_match = self.heading_pattern.match(line)
            if heading_match:
                hashes, text = heading_match.groups()
                block = ContentBlock(
                    type=ContentType.HEADING,
                    raw_content=line,
                    level=len(hashes),
                    title=text.strip()
                )
                
                # 提取主标题作为文档标题
                if block.level == 1 and not result.title:
                    result.title = block.title
                    # 尝试从标题识别目标模块
                    result.target_module = self._detect_target_module(block.title)
                
                result.blocks.append(block)
                i += 1
                continue
            
            # 检测表格
            if stripped.startswith('|') and '|' in stripped[1:]:
                table_lines, i = self._extract_table(lines, i)
                if table_lines:
                    block = ContentBlock(
                        type=ContentType.TABLE,
                        raw_content='\n'.join(table_lines),
                        metadata={'row_count': len(table_lines)}
                    )
                    result.blocks.append(block)
                continue
            
            # 检测代码块
            if stripped.startswith('```'):
                code_lines, i = self._extract_code_block(lines, i)
                block = ContentBlock(
                    type=ContentType.CODE_BLOCK,
                    raw_content='\n'.join(code_lines),
                    metadata={'language': stripped[3:].strip()}
                )
                result.blocks.append(block)
                continue
            
            # 检测列表
            if self.list_pattern.match(line):
                list_lines, i = self._extract_list(lines, i)
                block = ContentBlock(
                    type=ContentType.LIST,
                    raw_content='\n'.join(list_lines)
                )
                result.blocks.append(block)
                continue
            
            # 默认为段落
            para_lines, i = self._extract_paragraph(lines, i)
            block = ContentBlock(
                type=ContentType.PARAGRAPH,
                raw_content='\n'.join(para_lines)
            )
            result.blocks.append(block)
        
        # 进一步分析目标位置
        self._analyze_target(result)
        
        return result
    
    def _extract_table(self, lines: List[str], start: int) -> tuple:
        """提取表格内容"""
        table_lines = []
        i = start
        
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue
            
            if line.startswith('|') and '|' in line[1:]:
                table_lines.append(lines[i])
                i += 1
            else:
                break
        
        # 验证是否为有效表格（至少包含分隔行）
        if len(table_lines) >= 2:
            has_sep = any(self.table_sep_pattern.match(l.strip()) 
                         for l in table_lines)
            if has_sep:
                return table_lines, i
        
        # 不是有效表格，返回第一行作为段落
        return [lines[start]], start + 1
    
    def _extract_code_block(self, lines: List[str], start: int) -> tuple:
        """提取代码块"""
        code_lines = [lines[start]]
        i = start + 1
        
        while i < len(lines):
            code_lines.append(lines[i])
            if lines[i].strip() == '```':
                i += 1
                break
            i += 1
        
        return code_lines, i
    
    def _extract_list(self, lines: List[str], start: int) -> tuple:
        """提取列表"""
        list_lines = []
        i = start
        
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            if not stripped:
                # 检查下一行是否继续列表
                if i + 1 < len(lines) and self.list_pattern.match(lines[i + 1]):
                    i += 1
                    continue
                break
            
            if self.list_pattern.match(line):
                list_lines.append(line)
                i += 1
            elif line.startswith(' ') or line.startswith('\t'):
                # 列表项的续行
                list_lines.append(line)
                i += 1
            else:
                break
        
        return list_lines, i
    
    def _extract_paragraph(self, lines: List[str], start: int) -> tuple:
        """提取段落"""
        para_lines = []
        i = start
        
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            if not stripped:
                i += 1
                break
            
            # 检查是否是其他类型的开始
            if (self.heading_pattern.match(line) or
                (stripped.startswith('|') and '|' in stripped[1:]) or
                stripped.startswith('```') or
                self.list_pattern.match(line)):
                break
            
            para_lines.append(line)
            i += 1
        
        return para_lines, i
    
    def _detect_target_module(self, title: str) -> Optional[str]:
        """从标题检测目标模块"""
        # 常见模块关键词映射
        module_keywords = {
            '泳道': '泳道',
            '工单': '工单中心',
            '变更': '变更管理',
            '漏洞': '安全漏洞',
            '工时': '工时填报',
        }
        
        for keyword, module in module_keywords.items():
            if keyword in title:
                return module
        
        return None
    
    def _analyze_target(self, content: ExtractedContent):
        """分析目标位置"""
        # 根据标题和内容分析目标章节
        for block in content.blocks:
            if block.type == ContentType.HEADING:
                title = block.title
                
                # 检测字段定义类内容
                if '字段' in title or 'field' in title.lower():
                    content.target_section = '工单字段'
                elif '规则' in title:
                    content.target_section = '业务规则'
                elif '状态' in title:
                    content.target_section = '状态定义'


def analyze_change_intent(content: str) -> Dict[str, Any]:
    """
    分析变更意图
    
    Args:
        content: 变更文档内容
        
    Returns:
        变更意图分析结果
    """
    extractor = ContentExtractor()
    extracted = extractor.extract(content)
    
    # 识别主要变更类型
    intent = {
        'type': 'unknown',
        'target_module': extracted.target_module,
        'target_section': extracted.target_section,
        'has_tables': len(extracted.get_tables()) > 0,
        'table_count': len(extracted.get_tables()),
        'heading_count': len(extracted.get_headings()),
    }
    
    # 判断变更类型
    headings = extracted.get_headings()
    for h in headings:
        title = h.title.lower()
        if '字段' in title:
            intent['type'] = 'field_definition'
            break
        elif '规则' in title:
            intent['type'] = 'rule_update'
            break
        elif '状态' in title:
            intent['type'] = 'state_update'
            break
    
    return intent


if __name__ == '__main__':
    # 测试
    test_doc = """# 创建泳道环境申请工单字段整理

根据实际工单数据整理的字段结构。

## 概览区域

| 字段 | 说明 |
|------|------|
| 名称 | 工单名称 |

## 详情区域

普通段落内容。

- 列表项1
- 列表项2
"""
    
    extractor = ContentExtractor()
    result = extractor.extract(test_doc)
    print(f"标题: {result.title}")
    print(f"目标模块: {result.target_module}")
    print(f"目标章节: {result.target_section}")
    print(f"块数: {len(result.blocks)}")
    for b in result.blocks:
        print(f"  - {b}")
