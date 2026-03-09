# 项目管理检查清单

## 项目创建检查清单

### Lightweight 模式

```markdown
- [ ] 1. 明确项目边界
  - 这个项目要解决什么问题？
  - 范围是什么（做什么、不做什么）？

- [ ] 2. 确定项目名称
  - 小写字母
  - 连字符分隔（如：my-project）
  - 无空格、无特殊字符

- [ ] 3. 创建目录结构
  - mkdir -p projects/{name}/
  - 复制 lightweight 模板文件

- [ ] 4. 填写 progress.md
  - 项目目标（一句话）
  - 当前状态
  - 待办清单（至少第一阶段）

- [ ] 5. 创建 decisions.md
  - 留空或填写已知的决策

- [ ] 6. 更新 TODO.md
  - 添加项目条目，标记为 lightweight 模式

- [ ] 7. 设定优先级
  - P0: 阻塞其他项目，必须立即做
  - P1: 重要，本周内完成
  - P2: 可以延后
```

### Engineering 模式

```markdown
- [ ] 1. 明确项目边界
  - 这个项目要解决什么问题？
  - 目标用户是谁？
  - 范围是什么（做什么、不做什么）？

- [ ] 2. 确定项目名称
  - 小写字母
  - 连字符分隔
  - 无空格、无特殊字符

- [ ] 3. 创建完整目录结构
  - mkdir -p projects/{name}/changes/
  - 复制 engineering 模板文件

- [ ] 4. 填写核心文档（初始版本）
  - [ ] progress.md - 项目概述和初始进度
  - [ ] requirements.md - 初始需求列表
  - [ ] architecture.md - 初步架构设计
  - [ ] iteration-plan.md - 第一个迭代规划
  - [ ] test-cases.md - 初始测试策略
  - [ ] decisions.md - 已知的架构决策
  - [ ] INTERRUPT.md - 初始状态

- [ ] 5. 创建空白的变更记录文件
  - [ ] changes/requirements.md
  - [ ] changes/architecture.md
  - [ ] tasks.md

- [ ] 6. 更新 TODO.md
  - 添加项目条目，标记为 engineering 模式
  - 包含关键文档链接

- [ ] 7. 确定依赖关系
  - 依赖哪些项目？
  - 被哪些项目依赖？

- [ ] 8. 设定优先级
  - P0/P1/P2
```

---

## 任务创建检查清单

```markdown
- [ ] 1. 识别类型
  - 这是一个新项目？→ 走"项目创建"流程
  - 这是一个任务？→ 继续

- [ ] 2. 确认所属项目
  - 这个任务属于哪个项目？
  - 如果无法确定，需要创建新项目

- [ ] 3. 添加到正确位置
  - lightweight: 添加到 projects/{name}/progress.md
  - engineering: 添加到 iteration-plan.md 或 tasks.md

- [ ] 4. 标记优先级
  - P0: 紧急，今天完成
  - P1: 重要，本周完成
  - P2: 一般，可以延后

- [ ] 5. 明确验收标准
  - 怎么算"完成"？
  - 需要验证什么？
  - engineering 模式：同步更新 test-cases.md
```

---

## 文档更新检查清单（Engineering 模式专用 - 精简版 2.0）

> **重要更新**: 遵循"规划与执行分离"原则，避免重复维护

### 新增/修改需求时

```markdown
- [ ] 1. 如果新增需求
  - [ ] 更新 requirements.md
  - [ ] 添加需求描述、优先级、验收标准

- [ ] 2. 如果修改已有需求
  - [ ] 在 changes/requirements.md 中记录变更
  - [ ] 说明变更原因和影响范围

- [ ] 3. 更新 progress.md（简要）
  - [ ] 在"最近完成"中添加需求变更记录
  - [ ] 不重复 requirements.md 的详细内容
```

### 开始新迭代时

```markdown
- [ ] 1. 创建/更新 iteration-plan.md（详细规划）
  - [ ] 迭代目标
  - [ ] 任务拆解（ID、名称、工时、依赖、验收标准）
  - [ ] 里程碑和时间线
  - [ ] ⚠️ **写完后冻结，迭代进行中不再修改**

- [ ] 2. 更新 progress.md（动态状态）
  - [ ] 标记新迭代为"当前迭代"
  - [ ] 更新整体进度百分比
  - [ ] 列出当前聚焦的任务
```

### 完成开发任务时

```markdown
- [ ] 1. 更新 progress.md（必须）
  - [ ] 在"最近完成"中添加任务完成记录（倒序）
  - [ ] 格式：时间 - 任务ID 完成
  - [ ] 简要描述关键成果（不重复 iteration-plan 详情）
  - [ ] 添加指标（测试数、覆盖率等）
  - [ ] 🔗 添加链接：详细规划见 iteration-plan.md#任务ID

- [ ] 2. 只更新 progress.md，不修改 iteration-plan.md
  - [ ] iteration-plan 在迭代结束后统一归档

- [ ] 3. 清理旧记录
  - [ ] "最近完成"只保留最近 3-5 条
  - [ ] 过多时归档到"历史记录"章节或删除
```

### 迭代结束时

```markdown
- [ ] 1. 归档 iteration-plan.md
  - [ ] 在顶部添加"已归档"标记
  - [ ] 记录实际完成时间
  - [ ] 对比原计划，记录偏差分析
  - [ ] 标记状态为 🟢 已完成

- [ ] 2. 更新 progress.md
  - [ ] 标记迭代为"已完成"
  - [ ] 更新整体进度
  - [ ] 简要总结迭代成果
```

### ❌ 禁止行为

```markdown
- [ ] 没有在 progress.md 复制 iteration-plan.md 的任务清单
- [ ] 没有在 iteration-plan.md 中频繁更新任务状态（应冻结）
- [ ] 没有创建 tasks.md（已废弃，内容并入 progress）
- [ ] progress.md 的"最近完成"没有堆积过多记录
- [ ] 没有在多个文档中重复描述同一个任务
```

---

## 旧版文档更新检查清单（废弃，仅供参考）

### 新增需求时（旧版）

### 新增需求时

```markdown
- [ ] 1. 更新 requirements.md
  - 添加需求描述
  - 标注优先级（P0/P1/P2）
  - 定义验收标准

- [ ] 2. 如果修改了已有需求
  - 在 changes/requirements.md 中记录变更
  - 说明变更原因
  - 分析影响范围

- [ ] 3. 更新 progress.md
  - 标记相关任务状态
  - 如有阻塞，记录阻塞原因
```

### 确定技术方案时

```markdown
- [ ] 1. 更新 architecture.md
  - 添加/修改模块设计
  - 更新接口定义
  - 添加架构图或说明

- [ ] 2. 记录关键决策
  - 在 decisions.md 中记录技术选型
  - 说明选择原因和权衡

- [ ] 3. 如果修改了已有架构
  - 在 changes/architecture.md 中记录变更
  - 说明变更原因
  - 提供兼容性/迁移方案
```

### 完成开发任务时

```markdown
- [ ] 1. 更新 tasks.md
  - 记录任务完成时间
  - 描述实现方案
  - 记录遇到的问题和解决方案

- [ ] 2. 更新 iteration-plan.md
  - 标记任务为完成
  - 更新迭代进度百分比

- [ ] 3. 更新 progress.md
  - 更新整体进度
  - 记录执行摘要
```

### 编写测试时

```markdown
- [ ] 1. 更新 test-cases.md
  - 添加测试用例描述
  - 定义测试数据
  - 明确预期结果
  - 标注测试类型（单元/集成/E2E）

- [ ] 2. 如果测试发现需求/设计问题
  - 回滚更新 requirements.md 或 architecture.md
  - 在 changes/ 中记录变更
```

---

## 对话结束检查清单（Engineering 模式强制）

每次对话结束前，必须完成以下检查：

```markdown
## 工作完成检查

- [ ] 1. 本次对话完成的工作
  - [ ] 在 tasks.md 中记录已完成的任务
  - [ ] 在 iteration-plan.md 中更新任务状态
  - [ ] 在 progress.md 中更新整体进度

## 文档更新检查

- [ ] 2. 需求相关变更？
  - [ ] 新增/修改了需求 → 更新 requirements.md
  - [ ] 修改了已有需求 → 在 changes/requirements.md 中记录

- [ ] 3. 架构相关变更？
  - [ ] 新增/修改了设计 → 更新 architecture.md
  - [ ] 修改了已有架构 → 在 changes/architecture.md 中记录
  - [ ] 做了技术决策 → 更新 decisions.md

- [ ] 4. 测试相关？
  - [ ] 新增/修改了测试 → 更新 test-cases.md

## 关键文档 Review 检查（阻塞进度）

- [ ] 5. 是否更新了关键文档？（需用户 Review 通过后才能继续）
  - [ ] requirements.md 新增/更新？
    - 是 → 提示用户 Review，等待 "Review 通过" 确认
    - 否 → 继续
  - [ ] architecture.md 新增/更新？
    - 是 → 提示用户 Review，等待 "Review 通过" 确认
    - 否 → 继续
  - [ ] progress.md 首次拆分 Iteration/task？
    - 是 → 提示用户 Review，等待 "Review 通过" 确认
    - 否 → 继续

- [ ] 6. 用户是否已确认关键文档 Review 通过？
  - [ ] 如未通过，记录修改意见，返回修改
  - [ ] 如已通过，继续下一步

## 重要文档检查提醒（不阻塞进度）

- [ ] 7. 是否更新了重要文档？（提醒用户检查，不阻塞）
  - [ ] progress.md 更新？
    - 是 → 提醒用户检查，列出本次更新摘要（3-5点）
    - 否 → 继续
  - [ ] decisions.md 更新？
    - 是 → 提醒用户检查，列出本次新增决策
    - 否 → 继续

- [ ] 8. 是否已提醒用户检查重要文档？
  - 格式："【重要文档已更新】xxx.md，建议检查："
  - 继续下一步（不等待确认）

## 状态记录检查

- [ ] 9. 更新 INTERRUPT.md
  - [ ] 记录当前阶段
  - [ ] 列出已完成的部分
  - [ ] 列出待恢复的部分
  - [ ] 记录任何阻塞问题

- [ ] 10. 进度总结
  - [ ] 当前整体进度百分比
  - [ ] 是否有阻塞问题
  - [ ] 下一步行动计划
```

---

## 项目完成检查清单

### Lightweight 模式

```markdown
- [ ] 1. 功能完整
  - 所有计划的功能已实现
  - 没有遗留的占位符

- [ ] 2. 基本测试通过
  - 手动测试通过

- [ ] 3. 文档完整
  - progress.md 已更新为完成状态
  - 关键决策已记录

- [ ] 4. 更新 TODO.md
  - 标记为 🟢 已完成
```

### Engineering 模式

```markdown
- [ ] 1. 功能完整
  - 所有计划的功能已实现
  - 没有遗留的占位符

- [ ] 2. 测试通过
  - [ ] 单元测试通过
  - [ ] 集成测试通过
  - [ ] 手动测试通过
  - [ ] test-cases.md 中所有用例已执行

- [ ] 3. 实际运行验证
  - 在生产环境（或等效环境）运行过
  - 没有明显错误

- [ ] 4. 文档完整
  - [ ] progress.md 已更新为完成状态
  - [ ] requirements.md 已归档最终版本
  - [ ] architecture.md 已反映最终架构
  - [ ] iteration-plan.md 所有迭代已完成
  - [ ] test-cases.md 测试用例完整
  - [ ] changes/ 变更记录完整
  - [ ] tasks.md 执行记录完整
  - [ ] decisions.md 关键决策已记录

- [ ] 5. 依赖检查
  - 阻塞的项目已完成
  - 下游项目已通知

- [ ] 6. 归档准备
  - 确定是否需要归档
  - 更新 TODO.md 状态为 🟢 已完成
```

---

## 层级规范检查清单

### TODO.md 检查

```markdown
- [ ] 只有项目列表，没有任务细节
- [ ] 每个项目都有链接
- [ ] 包含模式标记（lightweight/engineering）
- [ ] 包含状态徽章（🟡/🟢/🔴）
- [ ] 包含最后更新时间
```

### Engineering 项目检查

```markdown
## 必需文件检查
- [ ] progress.md 存在
- [ ] decisions.md 存在
- [ ] INTERRUPT.md 存在
- [ ] requirements.md 存在
- [ ] architecture.md 存在
- [ ] iteration-plan.md 存在
- [ ] test-cases.md 存在
- [ ] changes/requirements.md 存在
- [ ] changes/architecture.md 存在
- [ ] tasks.md 存在

## 文档时效性检查（工程模式）
- [ ] progress.md 最近 3 轮对话内更新过
- [ ] 如果进行了需求讨论，requirements.md 已更新
- [ ] 如果进行了技术讨论，architecture.md 或 decisions.md 已更新
- [ ] 如果完成了任务，tasks.md 已更新

## 内容质量检查
- [ ] progress.md 有明确的项目目标
- [ ] progress.md 有当前状态摘要（含百分比）
- [ ] requirements.md 有明确的验收标准
- [ ] architecture.md 有模块关系说明
- [ ] iteration-plan.md 有迭代目标和时间线
- [ ] test-cases.md 有预期结果定义
```

---

## 文档位置检查清单（防重复/防错位）

**在创建任何文档前，必须执行此检查：**

```markdown
- [ ] 1. 搜索现有文档
  - [ ] 执行: `find . -name "*.md" -type f | grep -i 文档名`
  - [ ] 确认是否已存在同名文档
  - [ ] 如果存在，更新而非创建

- [ ] 2. 确认文档类型和位置
  - [ ] 项目进度 → `projects/{name}/progress.md`
  - [ ] 需求文档 → `docs/requirements/` 或 `projects/{name}/requirements.md`
  - [ ] 架构文档 → `docs/design/` 或 `projects/{name}/architecture.md`
  - [ ] 变更记录 → `projects/{name}/changes/` 或 `docs/records/`
  - [ ] 不确定时 → 查看 `.agents/skills/project-management/DOCUMENT_INDEX.md`

- [ ] 3. 确认项目模式
  - [ ] lightweight: 文档在 `projects/{name}/` 下
  - [ ] engineering: 检查 `projects/{name}/` 和 `docs/` 的对应关系

- [ ] 4. 更新文档索引
  - [ ] 如果是新文档类型 → 更新 `DOCUMENT_INDEX.md`
  - [ ] 如果移动了文档 → 更新 `DOCUMENT_INDEX.md`
```

## 禁止行为检查清单

```markdown
- [ ] 没有在 TODO.md 直接写任务
- [ ] 没有创建缺少 progress.md 的项目
- [ ] engineering 项目没有缺少必需文档
- [ ] 没有在 A 项目写 B 项目的内容
- [ ] 没有把日常笔记写入 decisions.md
- [ ] 没有标记虚假的完成状态
- [ ] 项目名称符合规范（小写、连字符）
- [ ] engineering 项目没有超过 3 轮对话不更新文档
- [ ] **没有在未搜索的情况下创建新文档** ⭐ 新增
- [ ] **没有在错误位置创建 progress.md** （应在 projects/ 下，而非 docs/records/）⭐ 新增
```
