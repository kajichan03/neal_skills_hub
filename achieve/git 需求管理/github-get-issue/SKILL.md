---
name: github-get-issue
description: 获取 GitHub 单个 Issue 的完整详情，包括标题、正文、评论、标签、状态等。当用户问"issue #N 是什么"、"查看 issue 详情"、"获取 issue 内容"、"issue 123 说了什么"时触发。适用于需要详细了解某个 issue 内容、准备修复前查看需求、或查看 issue 讨论历史。提供脚本和命令两种方式。
---

# GitHub Issue 详情获取助手

获取单个 GitHub Issue 的完整信息，包括正文、评论、标签等。

## 触发条件

用户提到以下关键词时触发：
- "issue #N 详情" / "查看 issue #N"
- "获取 issue 内容" / "issue 说了什么"
- "看看 issue 123" / "issue 编号"
- "读取 issue" / "加载 issue"

## 使用方式

### 方式一：使用脚本（推荐）

```bash
./scripts/get-issue.sh <issue-number>
```

**示例**：
```bash
./scripts/get-issue.sh 42
```

### 方式二：直接使用 gh 命令

```bash
# 简洁查看
gh issue view <number>

# 查看完整信息（包括评论）
gh issue view <number> --comments

# JSON 格式（便于程序处理）
gh issue view <number> --json number,title,state,body,author,createdAt,updatedAt,labels,comments,url

# 查看并同时显示评论
gh issue view <number> --comments
```

## 输出内容

脚本输出的结构化信息包括：

- **基本信息**：编号、标题、状态（open/closed）
- **元数据**：作者、创建时间、更新时间、URL
- **标签**：所有标签列表
- **正文**：完整的 issue 描述
- **评论列表**：所有评论内容和时间

## 使用场景

### 场景 1：准备修复前查看需求

```bash
./scripts/get-issue.sh 42
```

阅读 issue 内容，理解问题和期望的修复方案。

### 场景 2：查看 issue 讨论历史

```bash
gh issue view 42 --comments
```

了解之前的讨论和决策过程。

### 场景 3：获取结构化数据用于脚本处理

```bash
gh issue view 42 --json number,title,state,body,labels
```

## 前置要求

- GitHub CLI (`gh`) 已安装并登录
- 当前目录是 Git 仓库，且关联了 GitHub 远程仓库

## 错误处理

如果获取失败：
1. 检查 issue 编号是否正确
2. 确认有权限访问该仓库
3. 检查 `gh auth status`

## 示例对话

**用户**：issue #42 是什么内容？

**助手**：我来获取 issue #42 的详情：

```bash
./scripts/get-issue.sh 42
```

**输出示例**：

```json
{
  "number": 42,
  "title": "登录页面超时问题",
  "state": "OPEN",
  "author": { "login": "alice" },
  "createdAt": "2024-03-15T10:30:00Z",
  "labels": [{ "name": "bug" }, { "name": "priority:high" }],
  "body": "## 问题描述...",
  "comments": [...]
}
```

**用户**：查看带评论的完整 issue

**助手**：

```bash
gh issue view 42 --comments
```

---

**用户**：获取 issue 100 的标题和状态

**助手**：

```bash
gh issue view 100 --json number,title,state,labels
```
