---
name: github-add-comment
description: 为 GitHub Issue 添加评论，用于记录进展、更新状态、回复讨论或标记工作流阶段。当用户说"给 issue 加评论"、"回复 issue #N"、"在 issue 上记录"、"更新进展"时触发。支持单行评论和多行 Markdown 格式，适用于工作流状态更新、进展汇报、技术讨论等场景。
---

# GitHub Issue 评论助手

为指定 GitHub Issue 添加评论，支持各种场景：记录进展、回复讨论、标记工作流状态等。

## 触发条件

用户提到以下关键词时触发：
- "给 issue 加评论" / "评论 issue #N"
- "回复 issue" / "在 issue 上记录"
- "更新进展" / "标记状态"
- "添加评论" / "comment on issue"

## 使用方式

### 方式一：使用脚本（推荐）

```bash
./scripts/add-comment.sh <issue-number> "<评论内容>"
```

**示例**：
```bash
# 单行评论
./scripts/add-comment.sh 42 "已完成初步分析，问题根因是..."

# 多行评论（使用换行符）
./scripts/add-comment.sh 42 "## 进展更新
- [x] 完成代码审查
- [ ] 编写测试用例
- [ ] 部署到测试环境"
```

### 方式二：直接使用 gh 命令

```bash
# 简单评论
gh issue comment <number> --body "评论内容"

# 从文件读取评论内容
git issue comment <number> --body-file comment.md

# 使用编辑器编写评论
gh issue comment <number> --editor

# 添加评论并关闭 issue
gh issue comment <number> --body "已完成修复" --close
```

## 常用场景

### 场景 1：记录工作进展

```bash
./scripts/add-comment.sh 42 "## 今日进展
- 定位到问题在 auth.js:45
- 发现 token 验证逻辑存在竞态条件
- 明天将实施修复方案"
```

### 场景 2：标记工作流阶段

```bash
./scripts/add-comment.sh 42 "ARCH 完成，进入 DEV 阶段

修复方案：
1. 在 token 验证前添加同步锁
2. 更新缓存策略为原子操作
3. 添加重试机制"
```

### 场景 3：QA 测试反馈

```bash
./scripts/add-comment.sh 42 "## 测试结果

✅ 单元测试通过
✅ 集成测试通过
✅ 手动测试通过

QA 通过，进入 ARCH 复查阶段"
```

### 场景 4：关闭 Issue

```bash
gh issue comment 42 --body "问题已修复并通过验证，关闭 issue" --close
```

## 评论格式建议

### Markdown 格式支持

```bash
./scripts/add-comment.sh 42 "## 标题
**加粗** 和 *斜体*

- 列表项 1
- 列表项 2

\`\`\`javascript
// 代码块
const fix = true;
\`\`\`"
```

### 任务列表

```bash
./scripts/add-comment.sh 42 "## 检查清单
- [x] 代码审查
- [x] 测试覆盖
- [ ] 文档更新"
```

### 引用其他 Issue

```bash
./scripts/add-comment.sh 42 "修复方案参考 #38 的实现方式"
```

## 前置要求

- GitHub CLI (`gh`) 已安装并登录
- 当前目录是 Git 仓库，且关联了 GitHub 远程仓库
- 对 issue 有评论权限

## 错误处理

如果添加失败：
1. 检查 issue 编号是否正确
2. 确认有权限评论该 issue
3. 检查评论内容是否为空
4. 检查 `gh auth status`

## 示例对话

**用户**：给 issue 42 加个进展评论

**助手**：好的，请提供评论内容：

**用户**：已完成初步排查，问题定位在数据库连接池配置

**助手**：

```bash
./scripts/add-comment.sh 42 "已完成初步排查，问题定位在数据库连接池配置"
```

**输出**：
```
✅ 评论已添加到 issue #42
```

---

**用户**：在 issue 100 上标记 QA 通过

**助手**：

```bash
./scripts/add-comment.sh 100 "## QA 测试结果

- ✅ 功能测试通过
- ✅ 边界测试通过
- ✅ 回归测试通过

QA 通过，进入 ARCH 复查阶段"
```

---

**用户**：关闭 issue 50 并添加总结评论

**助手**：

```bash
gh issue comment 50 --body "## 修复总结

问题根因：内存泄漏由于未关闭的事件监听器
修复方案：在组件卸载时移除监听器
验证结果：已通过所有测试

感谢 @alice 的反馈！" --close
```
