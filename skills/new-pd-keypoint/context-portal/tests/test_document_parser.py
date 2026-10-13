"""测试文档解析器"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

import unittest
from document_parser import DocumentParser, find_module_path


class TestDocumentParser(unittest.TestCase):
    
    def setUp(self):
        self.parser = DocumentParser()
        self.test_doc = """# 产品上下文

## 1. 信息架构

架构内容

### 1.1 模块A

模块A内容

#### 1.1.1 子模块

子模块内容

## 2. 功能模块

### 2.4 工单中心

工单中心描述

#### 泳道新建

新建泳道描述

##### 功能描述

功能描述内容

##### 工单字段

字段内容

#### 泳道变更

变更描述

### 2.5 泳道管理

泳道管理描述
"""
    
    def test_parse_title(self):
        """测试解析标题"""
        result = self.parser.parse(self.test_doc)
        self.assertEqual(result.title, "产品上下文")
    
    def test_parse_headings_count(self):
        """测试解析标题数量 - 包含#产品上下文作为根"""
        result = self.parser.parse(self.test_doc)
        # 根标题是 #产品上下文，它有两个子标题 (## 1. 和 ## 2.)
        self.assertEqual(len(result.headings), 1)  # 根节点
        self.assertEqual(len(result.headings[0].children), 2)  # 两个子章节
    
    def test_find_heading_by_text(self):
        """测试通过文本查找标题"""
        result = self.parser.parse(self.test_doc)
        heading = result.find_heading("工单中心")
        self.assertIsNotNone(heading)
        self.assertIn("工单中心", heading.text)
    
    def test_find_path_simple(self):
        """测试通过路径查找标题"""
        result = self.parser.parse(self.test_doc)
        # 路径需要包含从根开始的所有层级
        heading = result.find_path(["产品上下文", "2. 功能模块"])
        self.assertIsNotNone(heading)
        self.assertIn("功能模块", heading.text)
    
    def test_find_path_nested(self):
        """测试通过嵌套路径查找标题"""
        result = self.parser.parse(self.test_doc)
        heading = result.find_path(["产品上下文", "2. 功能模块", "2.4 工单中心"])
        self.assertIsNotNone(heading)
        self.assertIn("工单中心", heading.text)
    
    def test_find_path_deep(self):
        """测试通过深层路径查找标题"""
        result = self.parser.parse(self.test_doc)
        heading = result.find_path(["产品上下文", "2. 功能模块", "2.4 工单中心", "泳道新建", "工单字段"])
        self.assertIsNotNone(heading)
        self.assertIn("工单字段", heading.text)
    
    def test_find_module_path(self):
        """测试查找模块路径"""
        result = self.parser.parse(self.test_doc)
        path = find_module_path(result, ["泳道新建"])
        self.assertIsNotNone(path)
        self.assertEqual(path[-1], "泳道新建")


class TestDocumentParserWithFixtures(unittest.TestCase):
    """使用fixtures进行测试"""
    
    def setUp(self):
        self.parser = DocumentParser()
        fixtures_dir = os.path.join(os.path.dirname(__file__), 'fixtures')
        
        with open(os.path.join(fixtures_dir, 'base_context.md'), 'r') as f:
            self.base_content = f.read()
    
    def test_base_context_structure(self):
        """测试基础文档结构"""
        result = self.parser.parse(self.base_content)
        self.assertEqual(result.title, "产品上下文")
        
        # 应该能找到工单中心
        ticket_center = result.find_heading("工单中心")
        self.assertIsNotNone(ticket_center)
    
    def test_base_context_lane_creation_path(self):
        """测试泳道新建路径 - 基于实际fixture结构"""
        result = self.parser.parse(self.base_content)
        
        # 实际结构: 产品上下文 > 2. 功能模块与用户场景 > 2.4 工单中心 > 功能点与规则 > 泳道新建
        heading = result.find_path(["产品上下文", "2. 功能模块与用户场景", "2.4 工单中心", "功能点与规则", "泳道新建"])
        self.assertIsNotNone(heading)
        
        # 验证找到的是正确的节点
        self.assertIn("泳道新建", heading.text)


if __name__ == '__main__':
    unittest.main()
