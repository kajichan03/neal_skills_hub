---
name: github-list-issues
description: 列出 GitHub 仓库中的 Issues，支持按状态、标签、作者筛选。当用户问"有哪些 issue"、"查看 issue 列表"、"列出所有 bug"、"看看 open 的 issue"时触发。快速展示 issue 概览，包括编号、标题、标签和状态。适用于快速了解项目当前待办事项或筛选特定类型的 issue。
---

# GitHub Issue 列表查询助手

快速列出 GitHub 仓库中的 issues，支持多种筛选条件。

## 触发条件

用户提到以下关键词时触发：
- "有哪些 issue" / "列出 issue"
- "查看 issue 列表" / "看看 issues"
- "open 的 issue" / "待处理的 bug"
- "按标签筛选" / "bug 列表"

## 使用方式

### 默认查询

列出所有 open 状态的 issues：

```bash
gh issue list --state open
```

### 按状态筛选

```bash
# 只看 open 的
gh issue list --state open

# 只看 closed 的
gh issue list --state closed

# 看所有的
gh issue list --state all
```

### 按标签筛选

```bash
# 只看 bug
gh issue list --label "bug"

# 只看 feature request
gh issue list --label "enhancement"

# 多标签组合（AND 关系）
gh issue list --label "bug" --label "priority:high"
```

### 按作者筛选

```bash
# 只看某人创建的
gh issue list --author "username"
```

### 限制数量

```bash
# 只看最近的 10 个
gh issue list --limit 10
```

### JSON 格式输出

```bash
# 获取结构化数据
gh issue list --json number,title,state,labels,author,createdAt
```

## 常用组合

```bash
# 查看待处理的高优先级 bug
gh issue list --label "bug" --label "priority:high" --state open

# 查看最近创建的 feature requests
gh issue list --label "enhancement" --state open --limit 5

# 查看我创建的 issues
gh issue list --author "@me" --state open
```

## 输出解读

默认输出格式：

```
NUMBER  TITLE                                      LABELS      STATE  AUTHOR
#42     登录页面无法访问                           bug         OPEN   alice
#41     添加数据导出功能                           enhancement OPEN   bob
#40     修复内存泄漏问题                           bug         CLOSED carol
```

## 前置要求

- GitHub CLI (`gh`) 已安装并登录
- 当前目录是 Git 仓库，且关联了 GitHub 远程仓库

## 下一步操作

列出 issues 后，用户可以：
- 查看某个 issue 详情 → 使用 `github-get-issue` skill
- 为 issue 添加评论 → 使用 `github-add-comment` skill
- 开始修复某个 issue → 使用 `github-issue-sync` skill（工作流模式）

## 示例对话

**用户**：看看有哪些 open 的 bug

**助手**：我来为您查询当前 open 状态的 bug issues：

```bash
gh issue list --label "bug" --state open
```

**输出示例**：

```
NUMBER  TITLE                        LABELS  STATE  AUTHOR
#42     登录超时问题                 bug     OPEN   alice
#38     数据导出失败                 bug     OPEN   bob
#35     页面加载缓慢                 bug     OPEN   carol
```

需要查看某个 issue 的详细信息吗？请告诉我 issue 编号。

---

**用户**：列出最近的 5 个 issues

**助手**：

```bash
gh issue list --limit 5
```

---

**用户**：看看我创建的待处理 issue

**助手**：

```bash
gh issue list --author "@me" --state open
```
