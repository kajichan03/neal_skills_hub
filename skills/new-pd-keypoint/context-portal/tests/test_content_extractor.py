"""测试内容提取器"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

import unittest
from content_extractor import ContentExtractor, analyze_change_intent


class TestContentExtractor(unittest.TestCase):
    
    def setUp(self):
        self.extractor = ContentExtractor()
    
    def test_extract_title(self):
        """测试提取标题"""
        doc = "# 测试文档\n\n内容"
        result = self.extractor.extract(doc)
        self.assertEqual(result.title, "测试文档")
    
    def test_extract_headings(self):
        """测试提取标题"""
        doc = """# 主标题

## 二级标题1

内容1

## 二级标题2

内容2
"""
        result = self.extractor.extract(doc)
        headings = result.get_headings()
        # 包含主标题和两个二级标题
        self.assertEqual(len(headings), 3)
        self.assertEqual(headings[1].title, "二级标题1")
    
    def test_extract_tables(self):
        """测试提取表格"""
        doc = """# 文档

| 列1 | 列2 |
|-----|-----|
| A   | B   |

段落
"""
        result = self.extractor.extract(doc)
        tables = result.get_tables()
        self.assertEqual(len(tables), 1)
    
    def test_detect_target_module_lane(self):
        """测试检测泳道模块"""
        doc = "# 创建泳道环境申请工单\n\n内容"
        result = self.extractor.extract(doc)
        self.assertEqual(result.target_module, "泳道")
    
    def test_detect_target_module_ticket(self):
        """测试检测工单模块"""
        doc = "# 工单中心字段整理\n\n内容"
        result = self.extractor.extract(doc)
        # 应该检测到工单或工单中心
        self.assertIn(result.target_module, ["工单", "工单中心"])


class TestContentExtractorWithFixtures(unittest.TestCase):
    """使用fixtures进行测试"""
    
    def setUp(self):
        self.extractor = ContentExtractor()
        fixtures_dir = os.path.join(os.path.dirname(__file__), 'fixtures')
        
        with open(os.path.join(fixtures_dir, 'change_lanefields.md'), 'r') as f:
            self.change_content = f.read()
    
    def test_extract_lane_fields(self):
        """测试提取泳道字段文档"""
        result = self.extractor.extract(self.change_content)
        
        self.assertEqual(result.title, "创建泳道环境申请工单字段整理")
        self.assertEqual(result.target_module, "泳道")
        
        # 应该提取到表格
        tables = result.get_tables()
        self.assertGreaterEqual(len(tables), 3)  # 概览、组件变更、中间件
    
    def test_analyze_change_intent(self):
        """测试分析变更意图"""
        intent = analyze_change_intent(self.change_content)
        
        self.assertEqual(intent['target_module'], "泳道")
        self.assertTrue(intent['has_tables'])
        self.assertGreater(intent['table_count'], 0)


if __name__ == '__main__':
    unittest.main()
