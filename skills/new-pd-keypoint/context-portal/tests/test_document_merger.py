"""测试文档合并器"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

import unittest
from document_merger import DocumentMerger, merge_documents, MergeStrategy


class TestDocumentMerger(unittest.TestCase):
    
    def setUp(self):
        self.merger = DocumentMerger()
    
    def test_merge_simple_append(self):
        """测试简单追加"""
        base = "# 文档\n\n## 章节1\n\n内容"
        change = "# 新内容\n\n新章节"
        
        result = self.merger.merge(base, change)
        self.assertTrue(result.success)
        self.assertIn("新章节", result.content)
    
    def test_merge_insert_under_heading(self):
        """测试在标题下插入"""
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
        
        result = self.merger.merge(base, change)
        self.assertTrue(result.success)
        # 应该能找到插入的内容
        self.assertIn("工单字段", result.content)


class TestDocumentMergerIntegration(unittest.TestCase):
    """集成测试 - 使用fixtures"""
    
    def setUp(self):
        self.merger = DocumentMerger()
        fixtures_dir = os.path.join(os.path.dirname(__file__), 'fixtures')
        
        with open(os.path.join(fixtures_dir, 'base_context.md'), 'r') as f:
            self.base_content = f.read()
        
        with open(os.path.join(fixtures_dir, 'change_lanefields.md'), 'r') as f:
            self.change_content = f.read()
        
        with open(os.path.join(fixtures_dir, 'expected_output.md'), 'r') as f:
            self.expected_content = f.read()
    
    def test_merge_lane_fields_to_correct_position(self):
        """
        核心测试：验证字段定义能合并到正确的位置
        
        期望：
        - 内容插入到 2.4 工单中心 > 泳道新建 > 工单字段 下
        - 而不是作为新章节追加
        """
        result = self.merger.merge(self.base_content, self.change_content)
        
        self.assertTrue(result.success, f"合并失败: {result.message}")
        
        # 关键验证1：内容应该包含工单字段表格
        self.assertIn("工单名称", result.content)
        self.assertIn("digit29251", result.content)  # 示例值
        
        # 关键验证2：不应该出现线性追加的错误模式
        # 错误模式会是：文档末尾出现 "## 3. 工单字段定义更新"
        lines = result.content.split('\n')
        
        # 找到"工单中心"的位置
        ticket_center_idx = None
        for i, line in enumerate(lines):
            if '工单中心' in line and line.startswith('#'):
                ticket_center_idx = i
                break
        
        self.assertIsNotNone(ticket_center_idx, "应该能找到工单中心章节")
        
        # 找到"工单字段"内容的位置
        field_content_idx = None
        for i, line in enumerate(lines):
            if '工单名称' in line:  # 字段表格中的内容
                field_content_idx = i
                break
        
        self.assertIsNotNone(field_content_idx, "应该能找到字段内容")
        
        # 字段内容应该在工单中心之后，而不是在文档末尾的新章节
        self.assertGreater(field_content_idx, ticket_center_idx,
                          "字段内容应该在工单中心章节内")
    
    def test_merge_preserves_structure(self):
        """验证合并不会破坏原有文档结构"""
        result = self.merger.merge(self.base_content, self.change_content)
        
        # 验证原有章节仍然保留
        self.assertIn("1. 信息架构图", result.content)
        self.assertIn("2.1 工时填报助手", result.content)
        self.assertIn("2.4 工单中心", result.content)
        self.assertIn("泳道新建", result.content)
        self.assertIn("泳道变更", result.content)
    
    def test_merge_strategy_selection(self):
        """验证合并策略选择正确"""
        from document_parser import DocumentParser
        from content_extractor import ContentExtractor, analyze_change_intent
        
        parser = DocumentParser()
        extractor = ContentExtractor()
        
        base_structure = parser.parse(self.base_content)
        extracted = extractor.extract(self.change_content)
        intent = analyze_change_intent(self.change_content)
        
        # 创建合并计划
        plan = self.merger._create_merge_plan(base_structure, extracted, intent)
        
        # 验证策略不是简单的APPEND
        self.assertNotEqual(plan.strategy, MergeStrategy.APPEND,
                           "不应该使用简单追加策略")
        
        # 验证目标路径包含工单中心
        self.assertTrue(
            any('工单' in p or '泳道' in p for p in plan.target_path),
            f"目标路径应该包含工单中心或泳道: {plan.target_path}"
        )


class TestMergeDocumentsFunction(unittest.TestCase):
    """测试便捷函数"""
    
    def test_merge_documents_function(self):
        """测试merge_documents便捷函数"""
        base = "# 文档\n\n## 章节\n\n内容"
        change = "# 更新\n\n新内容"
        
        result = merge_documents(base, change)
        self.assertIn("新内容", result)


if __name__ == '__main__':
    unittest.main()
