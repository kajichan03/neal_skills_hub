---
name: github-issue-sync
description: 按照 ARCH-DEV-QA-ARCH-PM 工作流规范处理 GitHub Issue。当用户说"修复 issue"、"处理 bug"、"解决 issue #N"、"开始修 issue"时触发。这是专门用于 Issue 修复工作流的 skill，严格按照 ARCH → DEV → QA → ARCH → PM → DONE 流程执行，每个阶段必须切换到对应模式。不适用于简单的 issue 查询或评论添加。
---

# GitHub Issue 工作流处理助手

按照标准化的 ARCH-DEV-QA-ARCH-PM 工作流处理 GitHub Issue 修复。

## 触发条件

用户提到以下关键词时触发：
- "修复 issue" / "处理 bug"
- "解决 issue #N" / "修 issue"
- "开始处理" / "修复 bug"

## ⚠️ 重要：必须使用工作流模式

当用户要求修复 issue 时，**严禁**在当前模式直接修改代码。必须按照以下工作流执行：

```
ARCH → DEV → QA → ARCH → PM → DONE
  ↑      ↑
  └──────┘（QA/ARCH 不通过时回退到 DEV）
```

## 工作流执行步骤

### Step 1: 获取 Issue 详情

首先获取 issue 的完整信息：

```bash
./scripts/get-issue.sh <issue-number>
```

或：

```bash
gh issue view <issue-number> --comments
```

### Step 2: 切换到 ARCH 模式（必须）

**必须**使用 `switch_mode` 工具切换到 `agent-architect` 模式：

```
switch_mode(agent-architect)
```

在 ARCH 阶段：
- 分析 issue 内容
- 排查问题根因
- 设计修复方案
- 评估影响范围

**完成后**添加评论：

```bash
./scripts/add-comment.sh <issue-number> "## ARCH 完成

**排查结果:**
- 问题根因: [描述]
- 影响范围: [描述]

**修复方案:**
1. [步骤1]
2. [步骤2]

**ARCH 完成，进入 DEV 阶段**"
```

### Step 3: 切换到 DEV 模式

使用 `switch_mode` 切换到 `agent-dev` 模式：

```
switch_mode(agent-dev)
```

在 DEV 阶段：
- 根据 ARCH 方案实施代码修复
- 提交代码改动

**完成后**添加评论：

```bash
./scripts/add-comment.sh <issue-number> "## DEV 完成

**改动文件:**
- [文件1]
- [文件2]

**改动范围:**
[描述修改内容]

**DEV 完成，进入 QA 阶段**"
```

### Step 4: 切换到 QA 模式

使用 `switch_mode` 切换到 `agent-test` 模式：

```
switch_mode(agent-test)
```

在 QA 阶段：
- 根据 DEV 提供的改动范围编写/执行测试
- 验证修复是否有效

**完成后**添加评论：

```bash
# QA 通过
./scripts/add-comment.sh <issue-number> "## QA 完成

**测试结果:**
- ✅ 测试用例1
- ✅ 测试用例2

**QA 通过，进入 ARCH 复查阶段**"

# QA 不通过（回退到 DEV）
./scripts/add-comment.sh <issue-number> "## QA 未通过

**问题:** [描述未通过的原因]

**QA 未通过，回退到 DEV 阶段"
```

### Step 5: 切换到 ARCH 复查模式

使用 `switch_mode` 切换到 `agent-architect` 模式：

```
switch_mode(agent-architect)
```

在 ARCH 复查阶段：
- 复查代码设计合理性
- 检查扩展性

**完成后**添加评论：

```bash
# ARCH 复查通过
./scripts/add-comment.sh <issue-number> "## ARCH 复查完成

**复查结果:** 设计合理，符合规范

**ARCH 复查通过，进入 PM 阶段**"

# ARCH 复查不通过（回退到 DEV）
./scripts/add-comment.sh <issue-number> "## ARCH 复查未通过

**问题:** [描述]

**ARCH 复查未通过，回退到 DEV 阶段"
```

### Step 6: 切换到 PM 模式

使用 `switch_mode` 切换到 `project-manager` 模式：

```
switch_mode(project-manager)
```

在 PM 阶段：
- 更新 issue 状态
- 关闭 issue（如果已修复）

**完成后**关闭 issue：

```bash
gh issue close <issue-number> --comment "## 修复完成

**总结:** [修复内容总结]

已通过 ARCH-DEV-QA-ARCH-PM 全流程验证，关闭 issue。"
```

## 模式对照表

| 阶段 | 模式 | switch_mode 参数 |
|------|------|-----------------|
| ARCH | Agent Architect | `agent-architect` |
| DEV | Agent Aware Dev | `agent-dev` |
| QA | Agent Aware Test | `agent-test` |
| PM | Project Manager | `project-manager` |

## 工作流规则

### ✅ 必须做的

1. **必须先获取 issue 详情**
2. **必须按顺序执行阶段**（ARCH → DEV → QA → ARCH → PM）
3. **必须切换到对应模式**（使用 `switch_mode`）
4. **必须在 issue 中添加阶段完成评论**
5. **必须标记阶段转换状态**（如"ARCH 完成，进入 DEV 阶段"）

### ❌ 禁止做的

- **禁止在当前模式直接修复代码**
- **禁止跳过 ARCH 阶段**
- **禁止不创建工作流评论**
- **禁止 QA/ARCH 不通过时不回退**

## 回退机制

当 QA 或 ARCH 复查不通过时，必须回退到 DEV 阶段重新修复：

```
ARCH → DEV → QA → ❌ → DEV（回退）
                     ↓
              QA → ARCH → ❌ → DEV（回退）
                              ↓
                        QA → ...
```

每次回退都必须：
1. 在 issue 中评论说明回退原因
2. 切换到 DEV 模式重新修复
3. 重新走 QA → ARCH 流程

## 快速参考

```bash
# 获取 issue 详情
./scripts/get-issue.sh <number>

# 添加评论
./scripts/add-comment.sh <number> "<内容>"

# 关闭 issue
gh issue close <number> --comment "<内容>"
```

## 示例对话

**用户**：修复 issue #42

**助手**：好的，我来按照工作流处理 issue #42。首先获取 issue 详情：

```bash
./scripts/get-issue.sh 42
```

（获取详情后）

现在切换到 **ARCH (agent-architect)** 模式进行问题分析和方案设计：

```
switch_mode(agent-architect)
```

**在 ARCH 模式完成分析后**，添加评论并标记完成：

```bash
./scripts/add-comment.sh 42 "## ARCH 完成

**排查结果:** 登录超时由数据库连接池配置不当导致
**修复方案:** 调整连接池大小和超时设置

**ARCH 完成，进入 DEV 阶段**"
```

然后切换到 **DEV (agent-dev)** 模式实施修复...

（继续后续流程）
