# 中断记录

> 项目: {name}  
> 模式: engineering

---

## 会话恢复检查清单

每次对话开始时，按此清单检查：

### 1. 阅读核心文档
- [ ] 阅读 [progress.md](./progress.md) 了解当前进度
- [ ] 阅读 [requirements.md](./requirements.md) 了解需求
- [ ] 阅读 [architecture.md](./architecture.md) 了解设计
- [ ] 阅读 [iteration-plan.md](./iteration-plan.md) 了解当前迭代任务

### 2. 检查上次状态
- [ ] 查看 "上次会话结束状态" 部分
- [ ] 确认上次标记的"待恢复"任务
- [ ] 检查是否有遗留的阻塞问题

### 3. 关键文档 Review 前置检查（强制）

- [ ] **上一轮是否更新了关键文档？**
  - [ ] requirements.md 更新？→ 用户是否已确认 Review 通过？
    - 是 → 继续
    - 否 → ⚠️ **提示："请先 Review 上一轮更新的 requirements.md"**
  - [ ] architecture.md 更新？→ 用户是否已确认 Review 通过？
    - 是 → 继续
    - 否 → ⚠️ **提示："请先 Review 上一轮更新的 architecture.md"**
  - [ ] progress.md（首次拆分）更新？→ 用户是否已确认 Review 通过？
    - 是 → 继续
    - 否 → ⚠️ **提示："请先 Review 上一轮更新的 progress.md"**

- [ ] **如有未 Review 通过的关键文档 → 暂停开发，先完成 Review**

### 3. 确认本次目标
- [ ] 明确本次对话要完成的任务
- [ ] 确认任务优先级
- [ ] 预估可能需要的文档更新

---

## 上次会话结束状态

**会话时间**: {timestamp}

### 已完成

- [ ] {列出已完成的步骤}

### 待恢复

- [ ] {列出未完成的部分}

### 当前阻塞

| 问题 | 状态 | 备注 |
|------|------|------|
| {问题描述} | 🔴 / 🟡 | {备注} |

---

## 会话结束更新模板

对话结束时，使用以下内容更新本文件：

```markdown
**会话时间**: YYYY-MM-DD HH:MM

### 已完成
- [x] {任务1}
- [x] {任务2}

### 待恢复
- [ ] {任务3}
- [ ] {任务4}

### 当前阻塞
| 问题 | 状态 | 备注 |
|------|------|------|
| {问题} | {状态} | {备注} |

### 下次会话建议
{建议从哪个任务开始，需要关注什么}
```

---

## 文档更新状态追踪

上次文档更新时间：

| 文档 | 最后更新 | 是否需要更新 |
|------|----------|--------------|
| progress.md | {date} | 否 |
| requirements.md | {date} | 否 |
| architecture.md | {date} | 否 |
| iteration-plan.md | {date} | 否 |
| test-cases.md | {date} | 否 |
| tasks.md | {date} | 否 |

---

*自动创建于: {timestamp}*
