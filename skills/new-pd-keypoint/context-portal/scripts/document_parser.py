"""
文档结构解析器

解析Markdown文档的层级结构，识别模块位置和标题体系
"""

import re
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple


@dataclass
class Heading:
    """文档标题节点"""
    level: int  # 1-6 对应 # - ######
    text: str
    line_number: int
    children: List['Heading'] = field(default_factory=list)
    content_lines: List[str] = field(default_factory=list)  # 该标题下的内容行
    parent: Optional['Heading'] = None  # 父节点引用
    
    @property
    def anchor(self) -> str:
        """生成锚点ID"""
        return re.sub(r'[^\w\s-]', '', self.text).strip().replace(' ', '-').lower()
    
    def __repr__(self):
        return f"Heading({self.level}# {self.text[:30]})"


@dataclass
class DocumentStructure:
    """文档结构树"""
    title: str = ""
    headings: List[Heading] = field(default_factory=list)
    raw_lines: List[str] = field(default_factory=list)
    
    def find_heading(self, text_pattern: str, level: Optional[int] = None) -> Optional[Heading]:
        """
        根据文本模式查找标题
        
        Args:
            text_pattern: 要匹配的文本（支持部分匹配）
            level: 可选，指定标题级别
            
        Returns:
            匹配的标题节点或None
        """
        for heading in self._flatten_headings(self.headings):
            if text_pattern in heading.text:
                if level is None or heading.level == level:
                    return heading
        return None
    
    def find_path(self, path_parts: List[str]) -> Optional[Heading]:
        """
        根据路径查找标题（如 ['2.4 工单中心', '泳道新建', '工单字段']）
        
        Args:
            path_parts: 路径各部分文本
            
        Returns:
            匹配的标题节点或None
        """
        current_headings = self.headings
        matched_heading = None
        
        for part in path_parts:
            found = None
            for heading in current_headings:
                if part in heading.text:
                    found = heading
                    break
            
            if found is None:
                return None
            
            matched_heading = found
            current_headings = found.children
        
        return matched_heading
    
    def get_insert_position(self, parent_heading: Heading, new_heading_level: int) -> int:
        """
        获取在父标题下插入新内容的位置
        
        Args:
            parent_heading: 父标题
            new_heading_level: 新标题的级别
            
        Returns:
            插入的行号
        """
        # 找到父标题的最后一行
        if parent_heading.children:
            # 如果有子标题，找到最后一个子标题的结束位置
            last_child = parent_heading.children[-1]
            return self._get_heading_end_line(last_child)
        else:
            # 如果没有子标题，返回父标题内容结束位置
            return parent_heading.line_number + len(parent_heading.content_lines)
    
    def _flatten_headings(self, headings: List[Heading]) -> List[Heading]:
        """扁平化所有标题"""
        result = []
        for h in headings:
            result.append(h)
            result.extend(self._flatten_headings(h.children))
        return result
    
    def _get_heading_end_line(self, heading: Heading) -> int:
        """获取标题内容的结束行号"""
        if heading.children:
            return self._get_heading_end_line(heading.children[-1])
        return heading.line_number + len(heading.content_lines)


class DocumentParser:
    """Markdown文档解析器"""
    
    HEADING_PATTERN = re.compile(r'^(#{1,6})\s+(.+)$')
    
    def parse(self, content: str) -> DocumentStructure:
        """
        解析Markdown文档
        
        Args:
            content: Markdown文本内容
            
        Returns:
            DocumentStructure 文档结构树
        """
        lines = content.split('\n')
        structure = DocumentStructure(raw_lines=lines)
        
        # 解析所有标题
        headings = []
        for i, line in enumerate(lines):
            match = self.HEADING_PATTERN.match(line)
            if match:
                hashes, text = match.groups()
                level = len(hashes)
                heading = Heading(level=level, text=text.strip(), line_number=i)
                headings.append(heading)
        
        # 构建树结构
        if headings:
            structure.title = headings[0].text if headings[0].level == 1 else ""
            structure.headings = self._build_tree(headings, lines)
        
        return structure
    
    def _build_tree(self, headings: List[Heading], lines: List[str]) -> List[Heading]:
        """构建标题树结构"""
        if not headings:
            return []
        
        # 构建索引：每个标题的开始和结束行
        for i, heading in enumerate(headings):
            # 找到该标题的内容结束位置（下一个同级或更高级标题前）
            end_line = len(lines)
            for j in range(i + 1, len(headings)):
                if headings[j].level <= heading.level:
                    end_line = headings[j].line_number
                    break
            heading.content_lines = lines[heading.line_number:end_line]
        
        # 构建树
        root_headings = []
        stack = []  # 用于跟踪父标题栈
        
        for heading in headings:
            # 弹出栈中级别大于等于当前标题的元素
            while stack and stack[-1].level >= heading.level:
                stack.pop()
            
            if stack:
                # 有父标题，添加到父标题的子节点
                parent = stack[-1]
                heading.parent = parent
                parent.children.append(heading)
            else:
                # 没有父标题，作为根节点
                root_headings.append(heading)
            
            # 当前标题入栈
            stack.append(heading)
        
        return root_headings
    
    def extract_section(self, structure: DocumentStructure, 
                       heading: Heading) -> str:
        """
        提取指定标题下的完整内容
        
        Args:
            structure: 文档结构
            heading: 目标标题
            
        Returns:
            该标题下的完整文本内容
        """
        start = heading.line_number
        end = self._get_section_end(structure, heading)
        return '\n'.join(structure.raw_lines[start:end])
    
    def _get_section_end(self, structure: DocumentStructure, 
                         heading: Heading) -> int:
        """获取章节结束位置"""
        if not heading.children:
            # 找到下一个同级或更高级标题
            for i in range(heading.line_number + 1, len(structure.raw_lines)):
                line = structure.raw_lines[i]
                match = self.HEADING_PATTERN.match(line)
                if match:
                    level = len(match.group(1))
                    if level <= heading.level:
                        return i
            return len(structure.raw_lines)
        else:
            # 有子标题，找到最后一个子标题的结束
            last_child = heading.children[-1]
            return self._get_section_end(structure, last_child)


def find_module_path(structure: DocumentStructure, 
                     module_keywords: List[str]) -> Optional[List[str]]:
    """
    根据关键词查找模块路径
    
    Args:
        structure: 文档结构
        module_keywords: 模块关键词列表，按优先级排序
        
    Returns:
        完整路径列表或None
    """
    def search_in_headings(headings: List[Heading], path: List[str]) -> Optional[List[str]]:
        for h in headings:
            current_path = path + [h.text]
            
            # 检查当前标题是否匹配
            for keyword in module_keywords:
                if keyword in h.text:
                    return current_path
            
            # 递归搜索子节点
            result = search_in_headings(h.children, current_path)
            if result:
                return result
        
        return None
    
    return search_in_headings(structure.headings, [])


if __name__ == '__main__':
    # 简单测试
    test_doc = """# 产品上下文

## 1. 模块A

内容A

### 1.1 子模块

子内容

## 2. 模块B

内容B
"""
    
    parser = DocumentParser()
    result = parser.parse(test_doc)
    print(f"标题: {result.title}")
    print(f"顶层标题数: {len(result.headings)}")
    
    for h in result.headings:
        print(f"  {h.level}# {h.text}, 子节点: {len(h.children)}")
        for ch in h.children:
            print(f"    {ch.level}# {ch.text}")
