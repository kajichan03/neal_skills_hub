# [项目名称] - 流程状态文档

> 由 ux-init skill 自动生成，由 ux-flow skill 维护更新

## 项目信息

| 字段 | 值 |
|------|-----|
| 项目名称 | [填写] |
| 创建时间 | [自动记录] |
| 当前阶段 | [阶段名称] |
| 上次更新时间 | [自动记录] |

## 流程阶段参考（来自 README.md）

| 阶段 | 名称 | 入口 Skill | 前置条件 | 产出文件 |
|------|------|-----------|---------|---------|
| 问题锚定 | ux-phase0-anchor | 用户有初步痛点描述 | 无 | 00-quick-anchor.md |
| 上下文补充 | ux-phase1-context | 有问题锚定输出 | 00-quick-anchor.md | 00-context.md |
| 方案研究 | ux-phase2-research | 需要调研解决方案 | 00-quick-anchor.md | 02-solution-research.md |
| 对抗式 Synthesis | ux-phase3-synthesis | 有足够调研信息 | 00-quick-anchor.md, 00-context.md, 02-solution-research.md | 03-synthesis.md |
| MVP 划定 | ux-phase4-mvp | 有 Synthesis 结论 | 03-synthesis.md | 04-mvp-scope.md |
| 用户旅程设计 | ux-phase5-user-journey | 有 MVP 范围 | 04-mvp-scope.md | 05-user-journey.md |
| 流程演示 Demo | ux-phase6-demo | 有用户旅程 | 05-user-journey.md | 06-flow-demo.html |
| BRD Demo Script（可选）| ux-brd-demo-coach | 有 Demo 输出 | 06-flow-demo.html | 06-brd-demo-script.md |
| 项目章程 | ux-phase7-project-goal | 有用户旅程和 MVP | 05-user-journey.md, 04-mvp-scope.md | 07-project-goal.md |
| 规则详细设计 | ux-phase8-rules | 有项目章程（含复杂功能点标记）| 07-project-goal.md | 更新 07-project-goal.md |
| 易用性检查 | ux-phase9-usability-check | 有项目章程 | 07-project-goal.md | 09-usability-checklist.md |
| 拆分设计任务 | ux-phase10-design-task-split | 有用户旅程和项目章程 | 05-user-journey.md, 07-project-goal.md | 10-design-tasks.md |
| 执行设计任务 | ux-phase10-design-task-execute | 有设计任务清单 | 10-design-tasks.md | 更新 10-design-tasks.md |
| PRD 生成 | ux-phase11-prd | 有项目章程 | 07-project-goal.md | 11-prd.md |
| 项目收尾 | ux-context-update-after-design-finish | 有 PRD | 11-prd.md | context-after.md |

## 阶段跳转规则

### 初始状态（无任何文件）
→ 建议执行 ux-phase0-anchor（问题锚定）

### 已有文件检测
- 有 00-quick-anchor.md，无 00-context.md → 建议执行 ux-phase1-context
- 有 00-quick-anchor.md，无 02-solution-research.md → 建议执行 ux-phase2-research
- 有 02-solution-research.md → 建议执行 ux-phase3-synthesis
- 有 03-synthesis.md → 建议执行 ux-phase4-mvp
- 有 04-mvp-scope.md → 建议执行 ux-phase5-user-journey
- 有 05-user-journey.md，无 06-flow-demo.html → 建议执行 ux-phase6-demo
- 有 06-flow-demo.html → 可选执行 ux-brd-demo-coach（BRD Demo Script），或直接进入 ux-phase7-project-goal
- 有 06-brd-demo-script.md → 建议执行 ux-phase7-project-goal
- 有 05-user-journey.md，有 04-mvp-scope.md，无 07-project-goal.md → 建议执行 ux-phase7-project-goal
- 有 07-project-goal.md（含复杂功能点标记）→ 建议执行 ux-phase8-rules
- 有 07-project-goal.md → 建议执行 ux-phase9-usability-check
- 有 07-project-goal.md 和 05-user-journey.md，无 10-design-tasks.md → 建议执行 ux-phase10-design-task-split
- 有 10-design-tasks.md → 建议执行 ux-phase10-design-task-execute
- 有 07-project-goal.md，无 11-prd.md → 建议执行 ux-phase11-prd
- 有 11-prd.md → 建议执行 ux-context-update-after-design-finish（项目收尾）

## 建议输入文档

为提升设计产出质量，建议准备以下输入文档：

| 文档 | 说明 | 优先级 |
|------|------|--------|
| `context.md` | 项目背景、技术栈、约束条件 | 推荐 |
| `page-structure-schema.md` | 页面结构 Schema 定义（标准模板） | 推荐 |
| `[product]-page-structures.md` | 具体产品的页面结构实例 | 可选 |

> 💡 **提示**：提供页面结构文档可显著提升 Demo 和原型生成质量。
> > 参考：`input/page-structure-schema.md`（可从 `latest/ux-page-structure/page-structure-schema.md` 复制）

---

## 当前项目状态（动态更新）

| 阶段 | 产出文件 | 完成时间 |
|------|---------|---------|
| [阶段名称] | [产出文件] | [完成时间] |