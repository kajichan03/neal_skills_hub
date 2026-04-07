---
name: ux-flow
description: 流程状态管理 - 读取流程状态文档，判断当前阶段，推荐下一步
license: MIT
compatibility: Any phase, requires flow-status.md
metadata:
  author: ux-workflow
  version: "1.0"
  workflow: user-centric-design
  phase: "flow"
---

## 什么时候使用

产品设计流程的任意阶段完成后，需要确定下一步应该执行什么时使用此 skill。

## 目标

读取流程状态文档，检测已有文件，判断当前阶段，推荐最合适的下一步。

## 核心功能

### 1. 读取流程状态

```bash
cat input/flow-status.md
```

提取：
- 项目名称
- 当前阶段
- 已完成的阶段列表
- 上次更新时间

### 2. 检测已有文件

扫描 `input/` 目录，检测以下产出文件是否存在：

```bash
ls -la input/*.md input/*.html 2>/dev/null
```

检测清单：

| 阶段 | 产出文件 |
|------|---------|
| 问题锚定 | 00-quick-anchor.md |
| 上下文补充 | 00-context.md |
| 方案研究 | 02-solution-research.md |
| 对抗式 Synthesis | 03-synthesis.md |
| MVP 划定 | 04-mvp-scope.md |
| 用户旅程设计 | 05-user-journey.md |
| 流程演示 Demo | 06-flow-demo.html |
| 项目章程 | 07-project-goal.md |
| 易用性检查 | 09-usability-checklist.md |
| 拆分设计任务 | 10-design-tasks.md |
| PRD 生成 | 11-prd.md |
| 项目收尾 | context-after.md |

### 3. 阶段判断逻辑

根据检测到的文件，匹配当前阶段：

| 检测条件 | 当前阶段 | 推荐下一步 |
|---------|---------|---------|
| 无文件 | 未开始 | 问题锚定 (ux-phase0-anchor) |
| 有 00-quick-anchor.md | 问题锚定已完成 | 上下文补充 (ux-phase1-context) |
| 有 00-quick-anchor.md, 00-context.md | 上下文补充已完成 | 方案研究 (ux-phase2-research) |
| 有 02-solution-research.md | 方案研究已完成 | 对抗式 Synthesis (ux-phase3-synthesis) |
| 有 03-synthesis.md | Synthesis 已完成 | MVP 划定 (ux-phase4-mvp) |
| 有 04-mvp-scope.md | MVP 已划定 | 用户旅程设计 (ux-phase5-user-journey) |
| 有 05-user-journey.md | 用户旅程已完成 | 流程演示 Demo (ux-phase6-demo) |
| 有 06-flow-demo.html | Demo 已完成 | 可选：BRD Demo Script (ux-brd-demo-coach) 或 项目章程 (ux-phase7-project-goal) |
| 有 05-user-journey.md, 04-mvp-scope.md | BRD Demo 完成 | 项目章程 (ux-phase7-project-goal) |
| 有 07-project-goal.md（含 🔍 标记）| 项目章程已完成 | 规则详细设计 (ux-phase8-rules) |
| 有 07-project-goal.md | 规则设计已完成 | 易用性检查 (ux-phase9-usability-check) |
| 有 07-project-goal.md, 05-user-journey.md | 易用性检查已完成 | 拆分设计任务 (ux-phase10-design-task-split) |
| 有 10-design-tasks.md | 任务拆分已完成 | 执行设计任务 (ux-phase10-design-task-execute) |
| 有 07-project-goal.md, 无 11-prd.md | 设计任务已完成 | PRD 生成 (ux-phase11-prd) |
| 有 11-prd.md | PRD 已生成 | 项目收尾 (ux-context-update-after-design-finish) |
| 有 context-after.md | 项目已收尾 | 流程结束，可开始新项目 |

### 4. 更新流程状态

每个阶段完成后，更新 flow-status.md：

1. **记录当前阶段完成**
   - 在"当前项目状态"表格中添加完成记录
   - 填写产出文件和完成时间

2. **更新当前阶段**
   - 将当前阶段标记为新阶段

3. **推荐下一步**
   - 基于检测到的文件，推荐最合适的下一步
   - 提供清晰的选项供用户选择

### 5. 输出示例

```
## 当前项目状态

| 阶段 | 产出文件 | 完成时间 |
|------|---------|---------|
| 问题锚定 | 00-quick-anchor.md | 2026-04-03 |
| 上下文补充 | 00-context.md | 2026-04-03 |

## 推荐下一步

根据检测到的文件（00-quick-anchor.md, 00-context.md），建议：

- **选项 A**：进入方案研究 → 运行 `/ux:phase2-research`
- **选项 B**：如需补充上下文 → 运行 `/ux:phase1-context`

请选择或输入其他需求。
```

---

## 护栏

- **必须先有 flow-status.md** - 如果不存在，引导用户先调用 ux-init
- **文件检测要准确** - 使用准确的产出文件名检测
- **阶段逻辑要清晰** - 按照检测表准确判断
- **更新要同步** - 阶段完成后必须更新 flow-status.md
- **推荐要具体** - 提供清晰的选项，不只是泛泛而谈

---

## 阶段对照表

| 阶段 | Skill | 说明 |
|------|-------|------|
| 问题锚定 | ux-phase0-anchor | 半天内对齐问题方向 |
| 上下文补充 | ux-phase1-context | 收集组织背景、技术栈 |
| 方案研究 | ux-phase2-research | 用户故事 + 业界方案调研 |
| 对抗式 Synthesis | ux-phase3-synthesis | 多 Agent 对抗 |
| MVP 划定 | ux-phase4-mvp | Must-have 筛选 |
| 用户旅程设计 | ux-phase5-user-journey | 完整用户旅程 |
| 流程演示 Demo | ux-phase6-demo | 可交互原型 |
| 项目章程 | ux-phase7-project-goal | 渐进式规则 |
| 规则详细设计 | ux-phase8-rules | 复杂功能点详细规则 |
| 易用性检查 | ux-phase9-usability-check | 易用性清单 |
| 拆分设计任务 | ux-phase10-design-task-split | 按旅程拆分任务 |
| 执行设计任务 | ux-phase10-design-task-execute | 循环执行设计 |
| PRD 生成 | ux-phase11-prd | 面向研发 |
| 项目收尾 | ux-context-update_after_design_finish | 更新 context |

## 下一步

此 skill 在检测完当前阶段后会推荐具体的下一步，用户可选择执行建议的 skill 或输入其他需求。