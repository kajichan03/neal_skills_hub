#!/usr/bin/env python3
"""
Context Portal - 活的上下文系统主入口

产品 & 代码双轨上下文管理

Usage:
    python scripts/context_portal.py product-context:init --path ./prd/
    python scripts/context_portal.py product-context:update --change ./changes/new-fields.md
    python scripts/context_portal.py code-context:init --repo ./src/
    python scripts/context_portal.py context:check-consistency --since HEAD~1
"""

import os
import sys
import argparse
import json
from datetime import datetime
from pathlib import Path

# 添加scripts目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from document_parser import DocumentParser
from content_extractor import ContentExtractor, analyze_change_intent
from document_merger import DocumentMerger, merge_documents


class ContextPortal:
    """Context Portal 主类"""
    
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.parser = DocumentParser()
        self.extractor = ContentExtractor()
        self.merger = DocumentMerger()
        
        # 默认文件路径
        self.context_file = self.base_dir / "product-context.md"
        self.db_file = self.base_dir / "context.db"
    
    def product_context_init(self, path: str = None, files: list = None) -> dict:
        """
        流程 1: 产品上下文冷启动
        
        Args:
            path: PRD 文档目录
            files: 指定的 PRD 文件列表
            
        Returns:
            处理结果
        """
        print("=" * 60)
        print("流程 1: 产品上下文冷启动")
        print("=" * 60)
        
        # 发现 PRD 文件
        if files:
            prd_files = [Path(f) for f in files.split(',')]
        elif path:
            prd_path = Path(path)
            prd_files = list(prd_path.glob("*.md"))
            prd_files.sort()
        else:
            # 默认查找当前目录
            prd_files = list(self.base_dir.glob("*prd*.md"))
            prd_files.extend(self.base_dir.glob("*PRD*.md"))
            prd_files.sort()
        
        if not prd_files:
            return {"success": False, "error": "未找到 PRD 文件"}
        
        print(f"发现 {len(prd_files)} 个 PRD 文件:")
        for f in prd_files:
            print(f"  - {f}")
        
        # 顺序处理 PRD 文件
        merged_content = ""
        for i, prd_file in enumerate(prd_files):
            print(f"\n处理 [{i+1}/{len(prd_files)}]: {prd_file}")
            
            with open(prd_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if i == 0:
                merged_content = content
            else:
                # 使用智能合并
                result = self.merger.merge(merged_content, content)
                if result.success:
                    merged_content = result.content
                    print(f"  ✓ {result.message}")
                else:
                    print(f"  ✗ 合并失败: {result.message}")
        
        # 保存结果
        output_file = self.base_dir / f"product-context-{datetime.now().strftime('%Y%m%d')}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(merged_content)
        
        # 同时保存为默认文件
        with open(self.context_file, 'w', encoding='utf-8') as f:
            f.write(merged_content)
        
        print(f"\n✓ 产品上下文已保存到: {output_file}")
        print(f"✓ 默认上下文文件: {self.context_file}")
        
        return {
            "success": True,
            "output_file": str(output_file),
            "prd_count": len(prd_files)
        }
    
    def product_context_update(self, change_file: str, iteration: str = None) -> dict:
        """
        流程 2: 产品上下文更新（智能合并）
        
        Args:
            change_file: 变更文档路径
            iteration: 迭代标识
            
        Returns:
            处理结果
        """
        print("=" * 60)
        print("流程 2: 产品上下文更新")
        print("=" * 60)
        
        # 检查基础文档
        if not self.context_file.exists():
            return {
                "success": False,
                "error": f"基础上下文文件不存在: {self.context_file}\n请先执行 product-context:init"
            }
        
        # 检查变更文档
        change_path = Path(change_file)
        if not change_path.exists():
            return {"success": False, "error": f"变更文件不存在: {change_file}"}
        
        print(f"基础文档: {self.context_file}")
        print(f"变更文档: {change_path}")
        
        # 读取文档
        with open(self.context_file, 'r', encoding='utf-8') as f:
            base_content = f.read()
        
        with open(change_path, 'r', encoding='utf-8') as f:
            change_content = f.read()
        
        # 分析变更意图
        print("\n分析变更意图...")
        intent = analyze_change_intent(change_content)
        print(f"  目标模块: {intent.get('target_module', '未知')}")
        print(f"  变更类型: {intent.get('type', 'unknown')}")
        print(f"  包含表格: {intent.get('has_tables', False)}")
        
        # 执行智能合并
        print("\n执行智能合并...")
        result = self.merger.merge(base_content, change_content)
        
        if not result.success:
            return {"success": False, "error": result.message}
        
        print(f"✓ {result.message}")
        
        # 显示合并计划
        if result.applied_plans:
            plan = result.applied_plans[0]
            print(f"\n合并策略: {plan.strategy.value}")
            print(f"目标路径: {' > '.join(plan.target_path) if plan.target_path else '(文档末尾)'}")
        
        # 保存结果
        backup_file = self.base_dir / f"product-context-backup-{datetime.now().strftime('%Y%m%d')}.md"
        
        # 备份旧版本
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(base_content)
        
        # 写入新版本
        with open(self.context_file, 'w', encoding='utf-8') as f:
            f.write(result.content)
        
        print(f"\n✓ 原版本已备份: {backup_file}")
        print(f"✓ 更新后的上下文: {self.context_file}")
        
        return {
            "success": True,
            "backup_file": str(backup_file),
            "message": result.message,
            "strategy": plan.strategy.value if result.applied_plans else "unknown",
            "target_path": plan.target_path if result.applied_plans else []
        }
    
    def preview_merge(self, change_file: str) -> dict:
        """
        预览合并结果（不实际修改文件）
        
        Args:
            change_file: 变更文档路径
            
        Returns:
            预览结果
        """
        print("=" * 60)
        print("合并预览")
        print("=" * 60)
        
        if not self.context_file.exists():
            return {"success": False, "error": f"基础上下文文件不存在: {self.context_file}"}
        
        change_path = Path(change_file)
        if not change_path.exists():
            return {"success": False, "error": f"变更文件不存在: {change_file}"}
        
        with open(self.context_file, 'r', encoding='utf-8') as f:
            base_content = f.read()
        
        with open(change_path, 'r', encoding='utf-8') as f:
            change_content = f.read()
        
        # 分析
        intent = analyze_change_intent(change_content)
        print(f"变更文档: {change_path}")
        print(f"目标模块: {intent.get('target_module', '未知')}")
        print(f"变更类型: {intent.get('type', 'unknown')}")
        
        # 执行合并（不保存）
        result = self.merger.merge(base_content, change_content)
        
        if result.success and result.applied_plans:
            plan = result.applied_plans[0]
            print(f"\n合并策略: {plan.strategy.value}")
            print(f"目标路径: {' > '.join(plan.target_path) if plan.target_path else '(文档末尾)'}")
            print(f"原因: {plan.reason}")
        
        return {
            "success": result.success,
            "message": result.message,
            "preview": result.content[:500] + "..." if len(result.content) > 500 else result.content
        }


def main():
    """主入口"""
    parser = argparse.ArgumentParser(
        description='Context Portal - 活的上下文系统',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  # 初始化产品上下文
  python scripts/context_portal.py product-context:init --path ./prd/
  
  # 更新产品上下文（智能合并）
  python scripts/context_portal.py product-context:update --change ./changes/lane-fields.md
  
  # 预览合并结果
  python scripts/context_portal.py product-context:preview --change ./changes/lane-fields.md
        '''
    )
    
    parser.add_argument(
        'command',
        choices=[
            'product-context:init',
            'product-context:update',
            'product-context:preview'
        ],
        help='要执行的命令'
    )
    
    parser.add_argument('--path', help='PRD 文档目录路径')
    parser.add_argument('--files', help='指定的 PRD 文件列表（逗号分隔）')
    parser.add_argument('--change', help='变更文档路径')
    parser.add_argument('--iteration', help='迭代标识')
    parser.add_argument('--base-dir', default='.', help='基础目录（默认当前目录）')
    
    args = parser.parse_args()
    
    # 创建 ContextPortal 实例
    portal = ContextPortal(base_dir=args.base_dir)
    
    # 执行命令
    if args.command == 'product-context:init':
        result = portal.product_context_init(path=args.path, files=args.files)
    
    elif args.command == 'product-context:update':
        if not args.change:
            print("错误: --change 参数是必需的")
            sys.exit(1)
        result = portal.product_context_update(args.change, iteration=args.iteration)
    
    elif args.command == 'product-context:preview':
        if not args.change:
            print("错误: --change 参数是必需的")
            sys.exit(1)
        result = portal.preview_merge(args.change)
    
    # 输出结果
    if result.get('success'):
        print("\n✓ 执行成功")
        if 'output_file' in result:
            print(f"  输出文件: {result['output_file']}")
    else:
        print(f"\n✗ 执行失败: {result.get('error', '未知错误')}")
        sys.exit(1)


if __name__ == '__main__':
    main()
