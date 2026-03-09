#!/usr/bin/env python3
"""
创建新项目工具

自动化创建项目结构并更新 TODO.md
支持 lightweight 和 engineering 两种模式
"""

import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# 自动检测 skill 目录
SKILL_DIR = Path(__file__).parent.parent
TEMPLATE_DIR = SKILL_DIR / "TEMPLATE"
TEMPLATE_ENGINEERING_DIR = SKILL_DIR / "TEMPLATE-ENGINEERING"

# 默认工作空间为当前目录的父目录（可根据实际情况调整）
WORKSPACE = Path.cwd()


def get_project_mode() -> str:
    """询问项目模式"""
    print("\n选择项目模式:")
    print("  1. lightweight - 轻量级项目（1-3天完成，简单文档）")
    print("  2. engineering - 软件工程项目（长期维护，完整文档体系）")
    
    while True:
        choice = input("请输入 (1/2): ").strip()
        if choice == "1":
            return "lightweight"
        elif choice == "2":
            return "engineering"
        print("无效选择，请重新输入")


def get_project_type() -> str:
    """询问项目类型"""
    print("\n选择项目类型:")
    print("  1. system - 系统内项目 (放到 SYSTEMS/{system}/projects/)")
    print("  2. independent - 独立项目 (放到 PROJECTS/)")
    print("  3. current - 当前目录项目 (放到 projects/)")
    
    while True:
        choice = input("请输入 (1/2/3): ").strip()
        if choice == "1":
            return "system"
        elif choice == "2":
            return "independent"
        elif choice == "3":
            return "current"
        print("无效选择，请重新输入")


def get_system_name() -> str:
    """询问所属系统"""
    systems_dir = WORKSPACE / "SYSTEMS"
    if not systems_dir.exists():
        print("未找到 SYSTEMS 目录，使用默认系统 'main'")
        return "main"
    
    systems = [d.name for d in systems_dir.iterdir() if d.is_dir()]
    
    if len(systems) == 0:
        print("SYSTEMS 目录为空，使用默认系统 'main'")
        return "main"
    
    if len(systems) == 1:
        print(f"自动选择系统: {systems[0]}")
        return systems[0]
    
    print("选择所属系统:")
    for i, sys_name in enumerate(systems, 1):
        print(f"  {i}. {sys_name}")
    
    while True:
        choice = input(f"请输入 (1-{len(systems)}): ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(systems):
                return systems[idx]
        except ValueError:
            pass
        print("无效选择")


def create_project(
    name: str, 
    project_type: str, 
    mode: str,
    system: Optional[str] = None
) -> bool:
    """创建新项目"""
    
    # 确定目标目录
    if project_type == "system":
        target_dir = WORKSPACE / "SYSTEMS" / system / "projects" / name
    elif project_type == "independent":
        target_dir = WORKSPACE / "PROJECTS" / name
    else:  # current
        target_dir = WORKSPACE / "projects" / name
    
    if target_dir.exists():
        print(f"❌ 项目 {name} 已存在: {target_dir}")
        return False
    
    # 选择模板目录
    template_dir = TEMPLATE_ENGINEERING_DIR if mode == "engineering" else TEMPLATE_DIR
    
    if not template_dir.exists():
        print(f"❌ 模板目录不存在: {template_dir}")
        return False
    
    # 创建目录
    target_dir.mkdir(parents=True)
    print(f"📁 创建目录: {target_dir}")
    
    # 复制模板文件
    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    files_copied = []
    
    for template_file in template_dir.rglob("*"):
        if template_file.is_file():
            # 计算相对路径
            rel_path = template_file.relative_to(template_dir)
            target_file = target_dir / rel_path
            
            # 创建父目录
            target_file.parent.mkdir(parents=True, exist_ok=True)
            
            # 读取并填充模板
            content = template_file.read_text(encoding="utf-8")
            
            # 替换占位符
            content = content.replace("{项目名称}", name)
            content = content.replace("{name}", name)
            content = content.replace("{date}", today)
            content = content.replace("{timestamp}", now)
            content = content.replace("{YYYY-MM-DD}", today)
            content = content.replace("{一句话描述项目目标}", "待填写")
            content = content.replace("{阶段名称}", "Phase 1")
            content = content.replace("{预计时间}", today)
            content = content.replace("{任务1}", "任务描述")
            content = content.replace("{任务2}", "任务描述")
            content = content.replace("{问题描述}", "无")
            content = content.replace("{描述}", "项目创建")
            content = content.replace("{完成的任务}", "创建项目结构")
            content = content.replace("{行动计划}", "开始执行")
            content = content.replace("{为什么依赖}", "待说明")
            content = content.replace("{为什么被依赖}", "待说明")
            
            # 保存文件
            target_file.write_text(content, encoding="utf-8")
            files_copied.append(rel_path)
    
    print(f"✅ 已创建 {len(files_copied)} 个文件")
    for f in files_copied:
        print(f"   - {f}")
    
    return True


def update_todo(
    name: str, 
    description: str, 
    project_type: str, 
    mode: str,
    system: Optional[str]
):
    """更新 TODO.md"""
    todo_file = WORKSPACE / "TODO.md"
    if not todo_file.exists():
        print("⚠️  TODO.md 不存在，跳过更新")
        return
    
    content = todo_file.read_text(encoding="utf-8")
    
    # 确定链接路径
    if project_type == "system":
        link_path = f"./SYSTEMS/{system}/projects/{name}/progress.md"
    elif project_type == "independent":
        link_path = f"./PROJECTS/{name}/progress.md"
    else:
        link_path = f"./projects/{name}/progress.md"
    
    # 构建新条目
    today = datetime.now().strftime("%Y-%m-%d")
    mode_badge = "🔧" if mode == "engineering" else "📦"
    
    new_entry = f"""### X. {name} {mode_badge}
**状态**: 🔴 未开始 (0%)
**模式**: {mode}

| 属性 | 值 |
|------|-----|
| **创建时间** | {today} |
| **目标** | {description} |
| **阻塞** | 无 |

**快速链接**:
- [项目进度]({link_path})
"""
    
    if mode == "engineering":
        new_entry += f"""- [需求文档]({link_path.replace('progress.md', 'requirements.md')})
- [架构设计]({link_path.replace('progress.md', 'architecture.md')})
"""
    
    new_entry += "\n---\n\n"
    
    # 找到插入点
    marker = "## 🚀 进行中的项目\n"
    if marker in content:
        parts = content.split(marker, 1)
        new_content = parts[0] + marker + "\n" + new_entry + parts[1]
        todo_file.write_text(new_content, encoding="utf-8")
        print("✅ 已更新 TODO.md")
    else:
        print("⚠️  无法在 TODO.md 中找到插入点，请手动添加")


def main():
    """主函数"""
    print("🚀 创建新项目\n")
    print("=" * 60)
    
    # 获取项目信息
    name = input("\n项目名称 (如: my-project): ").strip()
    if not name:
        print("❌ 项目名称不能为空")
        return 1
    
    description = input("项目目标描述: ").strip() or "待填写"
    
    # 选择模式
    mode = get_project_mode()
    
    # 选择类型
    project_type = get_project_type()
    
    system = None
    if project_type == "system":
        system = get_system_name()
    
    # 创建项目
    print(f"\n创建项目: {name}")
    print(f"模式: {mode}")
    print(f"类型: {project_type}")
    if system:
        print(f"系统: {system}")
    print()
    
    if not create_project(name, project_type, mode, system):
        return 1
    
    # 更新 TODO
    update_todo(name, description, project_type, mode, system)
    
    print("\n" + "=" * 60)
    print("✅ 项目创建完成！")
    print(f"\n下一步:")
    if mode == "engineering":
        print(f"  1. 编辑 {name}/requirements.md 完善需求")
        print(f"  2. 编辑 {name}/architecture.md 确定技术方案")
        print(f"  3. 编辑 {name}/iteration-plan.md 规划迭代")
        print(f"  4. 阅读 {name}/INTERRUPT.md 了解文档更新规范")
    else:
        print(f"  1. 编辑 {name}/progress.md 填写详细信息")
    print(f"  5. 运行检查: python {SKILL_DIR}/tools/check-structure.py")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
