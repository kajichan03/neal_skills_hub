#!/usr/bin/env python3
"""
项目结构检查工具

检查项目管理体系的结构健康
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple

# 工作空间根目录
WORKSPACE = Path("~/clawd").expanduser()


def check_todo_links() -> Tuple[List[str], List[str]]:
    """检查 TODO.md 中的链接是否有效
    
    Returns:
        (有效链接列表, 失效链接列表)
    """
    todo_file = WORKSPACE / "TODO.md"
    if not todo_file.exists():
        print("❌ TODO.md 不存在")
        return [], []
    
    content = todo_file.read_text()
    # 匹配 markdown 链接: [text](./path)
    links = re.findall(r'\[.*?\]\(\./(.*?)\)', content)
    
    valid = []
    broken = []
    
    for link in links:
        full_path = WORKSPACE / link
        if full_path.exists():
            valid.append(link)
        else:
            broken.append(link)
    
    return valid, broken


def check_orphan_projects() -> Tuple[List[Path], List[Path]]:
    """检查项目覆盖情况
    
    Returns:
        (已登记项目, 未登记项目)
    """
    # 获取所有项目目录
    projects_dir = WORKSPACE / "SYSTEMS" / "automation" / "projects"
    if not projects_dir.exists():
        return [], []
    
    actual_projects = [d for d in projects_dir.iterdir() if d.is_dir()]
    
    # 读取 TODO.md 中的项目
    todo_file = WORKSPACE / "TODO.md"
    todo_content = todo_file.read_text() if todo_file.exists() else ""
    
    registered = []
    orphan = []
    
    for project_dir in actual_projects:
        project_name = project_dir.name
        # 检查是否在 TODO 中被引用
        if project_name in todo_content:
            registered.append(project_dir)
        else:
            orphan.append(project_dir)
    
    return registered, orphan


def check_project_structure(project_dir: Path) -> List[str]:
    """检查单个项目的结构合规性
    
    Returns:
        问题列表
    """
    issues = []
    
    # 必须有的文件
    if not (project_dir / "progress.md").exists():
        issues.append(f"缺少 progress.md")
    
    # 可选但推荐的文件
    if not (project_dir / "decisions.md").exists():
        issues.append(f"缺少 decisions.md (可选)")
    
    return issues


def check_cross_references() -> List[str]:
    """检查交叉引用一致性"""
    issues = []
    
    # 检查项目中的 TODO 链接是否正确
    projects_dir = WORKSPACE / "SYSTEMS" / "automation" / "projects"
    if not projects_dir.exists():
        return issues
    
    for project_dir in projects_dir.iterdir():
        if not project_dir.is_dir():
            continue
        
        progress_file = project_dir / "progress.md"
        if not progress_file.exists():
            continue
        
        content = progress_file.read_text()
        
        # 检查 TODO 链接
        if "[总览 TODO]" in content:
            # 新路径应该是 ../../../../TODO.md
            if "../../TODO.md" in content and "../../../../TODO.md" not in content:
                issues.append(f"{project_dir.name}: TODO 链接路径可能错误")
    
    return issues


def main():
    """主函数"""
    print("🔍 检查项目结构健康\n")
    print("=" * 60)
    
    all_ok = True
    
    # 1. 检查 TODO.md 链接
    print("\n📋 检查 TODO.md 链接...")
    valid_links, broken_links = check_todo_links()
    print(f"  有效链接: {len(valid_links)} 个")
    if broken_links:
        print(f"  ❌ 失效链接: {len(broken_links)} 个")
        for link in broken_links[:5]:  # 只显示前5个
            print(f"     - {link}")
        all_ok = False
    else:
        print("  ✅ 所有链接有效")
    
    # 2. 检查项目登记情况
    print("\n📁 检查项目登记...")
    registered, orphan = check_orphan_projects()
    print(f"  已登记项目: {len(registered)} 个")
    if orphan:
        print(f"  ⚠️  未登记项目: {len(orphan)} 个")
        for proj in orphan:
            print(f"     - {proj.name}")
        all_ok = False
    else:
        print("  ✅ 所有项目已登记")
    
    # 3. 检查项目结构
    print("\n📂 检查项目结构...")
    projects_dir = WORKSPACE / "SYSTEMS" / "automation" / "projects"
    if projects_dir.exists():
        all_issues = []
        for project_dir in projects_dir.iterdir():
            if not project_dir.is_dir():
                continue
            issues = check_project_structure(project_dir)
            if issues:
                all_issues.append((project_dir.name, issues))
        
        if all_issues:
            print(f"  ⚠️  发现 {len(all_issues)} 个项目有问题:")
            for name, issues in all_issues:
                print(f"     {name}:")
                for issue in issues:
                    print(f"       - {issue}")
        else:
            print("  ✅ 所有项目结构合规")
    
    # 4. 检查交叉引用
    print("\n🔗 检查交叉引用...")
    ref_issues = check_cross_references()
    if ref_issues:
        print(f"  ⚠️  发现 {len(ref_issues)} 个问题:")
        for issue in ref_issues:
            print(f"     - {issue}")
        all_ok = False
    else:
        print("  ✅ 交叉引用一致")
    
    # 总结
    print("\n" + "=" * 60)
    if all_ok:
        print("✅ 项目结构健康")
        return 0
    else:
        print("⚠️  发现一些问题，建议修复")
        return 1


if __name__ == "__main__":
    sys.exit(main())
