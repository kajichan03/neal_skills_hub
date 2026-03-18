---
name: github-issue-sync
description: 管理 GitHub Issue 的全流程助手，支持提交 bug、查询打开 issue、以及按 ARCH-DEV-QA-ARCH-PM 工作流处理 issue。适用于 bug 追踪、issue 处理和项目进度管理。
---

# GitHub Issue 管理助手

管理 GitHub Issue 的全流程：提交 bug、查询 issue、按规范工作流处理 issue。

## When to use

- 需要提交 bug 到 GitHub Issue
- 需要查询当前打开的 issue 列表
- 需要按照标准工作流处理 issue（排查→修复→验证→验收→关闭）

## When NOT to use

- 项目没有配置 GitHub 仓库或 GitHub CLI
- 需要处理非 bug 类型的任务（如 feature request 应该走其他流程）

## Inputs required

1. **GitHub CLI (gh)** - 确保已安装并登录
2. **GitHub 仓库** - 当前项目关联的 GitHub 仓库

## 工作场景

### 场景一：提交 Bug

#### 1. 收集 Bug 信息

通过对话收集以下信息（逐项确认，信息不足时要求补充）：

**必需信息：**
- [ ] 问题标题（一句话描述）
- [ ] 问题描述（发生了什么）
- [ ] 复现步骤（如何触发）
- [ ] 期望结果（应该发生什么）
- [ ] 实际结果（实际发生了什么）

**可选信息：**
- [ ] 环境信息（OS、Python 版本、依赖版本等）
- [ ] 错误日志或截图
- [ ] 已尝试的解决方案

#### 2. 确认信息充足

信息不足时，明确告知缺失项并要求补充：
> "信息不足，需要补充：1) 复现步骤 2) 错误日志"

信息充足后，询问用户确认：
> "信息已收集完整，是否提交到 GitHub Issue？"

#### 3. 提交到 GitHub Issue

```bash
gh issue create \
  --title "[Bug] <问题标题>" \
  --body "## 问题描述
<描述>

## 复现步骤
<步骤>

## 期望结果
<期望>

## 实际结果
<实际>

## 环境信息
<环境>

## 错误日志
<details>
<summary>展开查看</summary>

\`\`\`
<日志>
\`\`\`
</details>" \
  --label "bug"
```

---

### 场景二：查询打开的 Issue

快速查询当前打开的 issue：

```bash
# 列出所有 open 的 issues
gh issue list --state open

# 按标签筛选
gh issue list --label "bug"

# 查看某个 issue 详情
gh issue view <issue-number>
```

---

### 场景三：处理 Issue

#### 前置检查

1. 确认 GitHub CLI 已登录
2. 获取目标 issue 详情：`gh issue view <number>`
3. 向用户确认要处理的 issue 编号

#### Issue 处理工作流

任务必须按照以下状态机执行：

```
ARCH → DEV → QA → ARCH → PM → DONE
  ↑      ↑
  └──────┘（QA/ARCH 不通过时回退到 DEV）
```

##### 阶段 1: ARCH (Agent Architect)

**调用方式:** 切换到 `agent-architect` 模式

**任务:**
- 查询 issue 详情和项目本地上下文
- 排查问题、分析根因
- 给出修复思路和方案
- 评估设计合理性和扩展性

**完成标志:**
- 在 issue 中添加评论，记录排查结果和修复思路
- 明确标记状态："ARCH 完成，进入 DEV 阶段"

**不通过时:** 回退到 DEV 重新修复

##### 阶段 2: DEV (Agent Aware Dev)

**调用方式:** 切换到 `agent-dev` 模式

**任务:**
- 根据 ARCH 的修复思路执行代码修复
- 为 QA 提供改动范围和影响范围

**完成标志:**
- 提交代码改动
- 在 issue 中添加评论，记录修复内容和改动文件
- 明确标记状态："DEV 完成，进入 QA 阶段"

##### 阶段 3: QA (Agent Aware Test)

**调用方式:** 切换到 `agent-test` 模式

**任务:**
- 根据 DEV 提供的改动范围编写/执行测试
- 验证修复是否有效
- 判断是否通过

**完成标志:**
- 在 issue 中添加评论，记录测试结果
- **通过**: 标记 "QA 通过，进入 ARCH 复查"
- **不通过**: 标记 "QA 未通过，回退到 DEV"，返回阶段 2

##### 阶段 4: ARCH 复查 (Agent Architect)

**调用方式:** 切换到 `agent-architect` 模式

**任务:**
- 复查修复代码的设计合理性
- 检查扩展性和规范符合度

**完成标志:**
- 在 issue 中添加评论，记录复查结果
- **通过**: 标记 "ARCH 复查通过，进入 PM 阶段"
- **不通过**: 标记 "ARCH 复查未通过，回退到 DEV"，返回阶段 2

##### 阶段 5: PM (Project Manager)

**调用方式:** 切换到 `project-manager` 模式

**任务:**
- 更新 issue 进度和总结
- 如果 issue 已修复，关闭它

**完成标志:**
- 在 issue 中添加最终总结评论
- 关闭 issue: `gh issue close <number> --comment "已完成修复并通过验证"`

---

## 快速参考命令

```bash
# 检查 gh 状态
gh auth status

# 查看仓库信息
gh repo view --json url,nameWithOwner

# 创建 issue
gh issue create --title "..." --body "..." --label "bug"

# 查看 issue 列表
gh issue list --state open

# 查看 issue 详情
gh issue view <number>

# 添加评论
gh issue comment <number> --body "..."

# 关闭 issue
gh issue close <number> --comment "..."

# 重新打开 issue
gh issue reopen <number>
```

## Troubleshooting

### gh: 未认证
运行 `gh auth login` 并选择 HTTPS 或 SSH 方式登录。

### issue 创建失败
- 检查是否有仓库写入权限
- 检查标题是否超过 256 字符

### 模式切换失败
- 确认目标模式名称拼写正确
- 使用 `switch_mode` 工具进行切换
