---
name: github-issue-sync
description: GitHub Issue 全流程管理助手。场景1：通过脚本提交 bug 到 GitHub Issue。场景2：通过脚本提交新需求到 GitHub Issue。场景3：查询打开的 issue 列表。场景4：按 ARCH-DEV-QA-ARCH-PM 工作流修复 issue（必须切换模式执行）。适用于 bug 追踪、issue 查询和规范化 issue 修复流程。
---

# GitHub Issue 管理助手

管理 GitHub Issue 的全流程：通过脚本提交 bug/需求、查询 issue、按规范工作流处理 issue。

## When to use

- 需要**提交 bug** 到 GitHub Issue
- 需要**提交新需求**到 GitHub Issue
- 需要**查询**当前打开的 issue 列表（可在当前模式执行）
- 需要按工作流**修复 issue**（必须切换到 agent-architect 模式开始）

## When NOT to use

- 项目没有配置 GitHub 仓库或 GitHub CLI
- **当前是 code 模式且用户要求修复 issue** - 此时应该使用 `switch_mode` 切换到 agent-architect 模式

## Inputs required

1. **GitHub CLI (gh)** - 确保已安装并登录
2. **GitHub 仓库** - 当前项目关联的 GitHub 仓库

## 工作场景

### 场景一：提交 Bug

通过脚本自动化提交 bug issue。

#### 1. 收集信息

通过对话收集以下信息：

**必需信息：**
- 问题标题（一句话描述）
- 问题描述（发生了什么）
- 复现步骤（如何触发）
- 期望结果（应该发生什么）
- 实际结果（实际发生了什么）

**可选信息：**
- 环境信息（OS、Python 版本等）
- 错误日志
- 已尝试的解决方案

#### 2. 执行脚本创建 Issue

信息收集完成后，执行脚本：

```bash
./scripts/create-bug.sh \
  "<问题标题>" \
  "<问题描述>" \
  "<复现步骤>" \
  "<期望结果>" \
  "<实际结果>" \
  "<环境信息>" \
  "<错误日志>"
```

> **注意**：所有参数需用双引号包裹，包含空格的内容会被正确处理。

---

### 场景二：提交新需求（Feature Request）

通过脚本自动化提交 feature request。

#### 1. 收集信息

通过对话收集以下信息：

**必需信息：**
- 需求标题（一句话描述）
- 现状（当前是什么情况）
- 问题（遇到了什么问题/痛点）
- 预期（希望达到什么效果）

**可选信息：**
- 优先级（高/中/低）
- 补充信息（建议方案、参考材料等）

#### 2. 执行脚本创建 Issue

信息收集完成后，执行脚本：

```bash
./scripts/create-feature.sh \
  "<需求标题>" \
  "<现状>" \
  "<问题>" \
  "<预期>" \
  "<优先级>" \
  "<补充信息>"
```

---

### 场景三：查询打开的 Issue

快速查询当前打开的 issue：

```bash
# 列出所有 open 的 issues
gh issue list --state open

# 按标签筛选
gh issue list --label "bug"
gh issue list --label "enhancement"

# 查看某个 issue 详情
gh issue view <issue-number>
```

---

### 场景四：处理 Issue（修复 Bug）

⚠️ **重要：此场景必须严格按照工作流执行，禁止在当前模式直接修复！**

#### 工作流入口

当用户说"修复 issue"、"处理 bug"、"解决 issue #N"等时：

1. **立即停止当前操作**
2. **切换到 ARCH (agent-architect) 模式开始排查**
3. 使用 `switch_mode` 工具切换到 agent-architect 模式

**禁止行为：**
- ❌ 在当前模式（如 code 模式）直接分析或修复代码
- ❌ 跳过 ARCH 阶段直接进入代码修改
- ❌ 不创建工作流评论直接提交修复

#### Issue 处理工作流（必须严格执行）

```
ARCH → DEV → QA → ARCH → PM → DONE
  ↑      ↑
  └──────┘（QA/ARCH 不通过时回退到 DEV）
```

---

##### 阶段 1: ARCH (Agent Architect) - 必须首先进入

**触发条件：** 用户要求修复 issue

**操作：使用 `switch_mode` 切换到 `agent-architect` 模式**

**任务：**
- 查询 issue 详情和项目本地上下文
- 排查问题、分析根因
- 给出修复思路和方案
- 评估设计合理性和扩展性

**完成标志：**
- 在 issue 中添加评论，记录：
  - 排查结果和根因分析
  - 修复思路和方案
  - 影响范围评估
- 明确标记状态：**"ARCH 完成，进入 DEV 阶段"**

---

##### 阶段 2: DEV (Agent Aware Dev)

**触发条件：** ARCH 阶段标记完成

**操作：使用 `switch_mode` 切换到 `agent-dev` 模式**

**任务：**
- 根据 ARCH 的修复思路执行代码修复
- 为 QA 提供改动范围和影响范围

**完成标志：**
- 提交代码改动
- 在 issue 中添加评论，记录：
  - 修复内容和改动文件
  - 改动范围说明
- 明确标记状态：**"DEV 完成，进入 QA 阶段"**

---

##### 阶段 3: QA (Agent Aware Test)

**触发条件：** DEV 阶段标记完成

**操作：使用 `switch_mode` 切换到 `agent-test` 模式**

**任务：**
- 根据 DEV 提供的改动范围编写/执行测试
- 验证修复是否有效
- 判断是否通过

**完成标志：**
- 在 issue 中添加评论，记录测试结果
- **通过**: 标记 **"QA 通过，进入 ARCH 复查"**
- **不通过**: 标记 **"QA 未通过，回退到 DEV"**，返回阶段 2

---

##### 阶段 4: ARCH 复查 (Agent Architect)

**触发条件：** QA 阶段标记通过

**操作：使用 `switch_mode` 切换到 `agent-architect` 模式**

**任务：**
- 复查修复代码的设计合理性
- 检查扩展性和规范符合度

**完成标志：**
- 在 issue 中添加评论，记录复查结果
- **通过**: 标记 **"ARCH 复查通过，进入 PM 阶段"**
- **不通过**: 标记 **"ARCH 复查未通过，回退到 DEV"**，返回阶段 2

---

##### 阶段 5: PM (Project Manager)

**触发条件：** ARCH 复查通过

**操作：使用 `switch_mode` 切换到 `project-manager` 模式**

**任务：**
- 更新 issue 进度和总结
- 如果 issue 已修复，关闭它

**完成标志：**
- 在 issue 中添加最终总结评论
- 关闭 issue: `gh issue close <number> --comment "已完成修复并通过验证"`

---

## 快速参考命令

```bash
# 检查 gh 状态
gh auth status

# 查看仓库信息
gh repo view --json url,nameWithOwner

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

## 脚本文件

- [`scripts/create-bug.sh`](scripts/create-bug.sh) - 创建 bug issue
- [`scripts/create-feature.sh`](scripts/create-feature.sh) - 创建 feature request issue

## Troubleshooting

### gh: 未认证
运行 `gh auth login` 并选择 HTTPS 或 SSH 方式登录。

### issue 创建失败
- 检查是否有仓库写入权限
- 检查标题是否超过 256 字符
- 检查脚本是否有执行权限：`chmod +x scripts/*.sh`

### 模式切换失败
- 确认目标模式名称拼写正确
- 使用 `switch_mode` 工具进行切换

## 工作流执行示例

### 示例：提交 bug

```
用户：记录一个 bug

系统响应：
好的，我来帮您记录 bug。请提供以下信息：

1. 问题标题：登录失败
2. 问题描述：用户无法使用正确凭据登录
3. 复现步骤：1. 打开登录页 2. 输入正确账号密码 3. 点击登录
4. 期望结果：登录成功，跳转到首页
5. 实际结果：提示"系统错误"

信息收集完成后：
./scripts/create-bug.sh \
  "登录失败" \
  "用户无法使用正确凭据登录" \
  "1. 打开登录页 2. 输入正确账号密码 3. 点击登录" \
  "登录成功，跳转到首页" \
  "提示系统错误" \
  "macOS, Chrome 120" \
  "Error: timeout at auth.js:42"
```

### 示例：提交需求

```
用户：记录一个新需求

系统响应：
好的，请提供以下信息：

1. 需求标题：添加导出功能
2. 现状：目前数据只能在线查看，无法导出
3. 问题：用户需要将数据保存到本地进行分析
4. 预期：支持导出 CSV 和 Excel 格式
5. 优先级：高

执行：
./scripts/create-feature.sh \
  "添加导出功能" \
  "目前数据只能在线查看，无法导出" \
  "用户需要将数据保存到本地进行分析" \
  "支持导出 CSV 和 Excel 格式" \
  "高" \
  "建议添加在数据表格右上角"
```

### 示例：修复 issue #1

```
用户：修复 issue #1

系统响应：
检测到用户需要修复 issue。根据工作流规范，我必须先切换到 agent-architect 模式进行排查。

使用 switch_mode 切换到 agent-architect 模式...
```

### 禁止的执行方式

```
用户：修复 issue #1

错误响应：
❌ 直接在当前 code 模式分析代码
❌ 不经过 ARCH 直接修复
❌ 不创建工作流评论
```
