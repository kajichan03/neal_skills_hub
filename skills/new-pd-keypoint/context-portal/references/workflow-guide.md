# Context Portal 工作流指南

> 四大流程的详细执行步骤和检查清单

---

## 流程 1: 产品上下文冷启动 (/product-context:init)

### 输入检查清单

- [ ] PRD 文档目录或文件列表已提供
- [ ] PRD 文件格式为 Markdown (.md)
- [ ] 如有 docx/pdf，先转换为 Markdown

### 执行步骤

#### Step 0: PRD 发现与排序

1. **扫描目录**
   ```
   扫描路径: {input_path}
   文件模式: *.md, *prd*.md, *需求*.md
   ```

2. **提取时间信息**
   - 优先从文件名提取日期: `prd-2024-01-15.md` → 2024-01-15
   - 其次从文件内容提取: 查找 "版本：v2.0 | 日期：2024-01-15"
   - 最后使用文件修改时间

3. **验证 PRD 完整性**
   - 检查必要的章节：功能需求、用户故事
   - 标记格式不规范的文档

#### Step 1: 顺序处理 PRD

按时间顺序逐个处理：

```
PRD #1 (最早) ──► Extract ──► Index ──► Export
PRD #2 ─────────► Extract ──► Merge ──► Export
PRD #3 (最新) ──► Extract ──► Merge ──► Export
```

**Extract 阶段**:
- 提取功能模块
- 提取用户场景
- 提取业务规则
- 提取状态定义
- 提取权限规则
- 提取页面结构

**Index 阶段**:
- 生成实体 ID
- 计算内容哈希
- 统计 token 数
- 存入 entities 表

**Merge 阶段**:
- 同名实体：内容哈希相同则跳过，不同则覆盖
- 新增实体：直接插入
- 更新关系表

**Export 阶段**:
- 生成 product-context-YYYY-MM-DD.md
- 更新 versions 表

### 输出检查清单

- [ ] product-context-YYYY-MM-DD.md 已生成
- [ ] context.db 已创建并包含实体数据
- [ ] 信息架构图已更新
- [ ] 所有功能模块已提取
- [ ] 用户场景表格完整
- [ ] 业务规则已提取

---

## 流程 2: 产品上下文更新 (/product-context:update)

### 输入检查清单

- [ ] 现有 context.db 存在
- [ ] 新 PRD/变更文档已提供
- [ ] 迭代标识（可选）

### 执行步骤

#### Step 0: 解析新 PRD

提取变更内容：
- 新增功能模块
- 修改的功能模块
- 删除的功能模块
- 新增业务规则
- 修改的业务规则

#### Step 1: 智能合并与冲突检测

**合并策略**:

| 变更类型 | 处理方式 | 示例 |
|---------|---------|------|
| 新增模块 | 直接插入 | 新增"泳道管理"模块 |
| 修改规则 | 对比差异，标记冲突 | 单次上限 100 → 1000 |
| 删除模块 | 标记 deprecated | 下线"旧版审批"功能 |

**冲突检测**:
- 检查同名实体内容差异
- 检查关键字矛盾（如数值变化）
- 检查依赖断裂

#### Step 2: 触发代码一致性检查（可选）

如果修改了业务规则且存在代码规则映射：
- 检查已有代码规则是否与新规则冲突
- 生成 code-sync-suggestions.md

### 输出检查清单

- [ ] 更新的 product-context-YYYY-MM-DD.md 已生成
- [ ] context.db 已更新
- [ ] 冲突报告（如有）
- [ ] 代码同步建议（如有）

---

## 流程 3: 代码规则提取 (/code-context:init 或 /code-context:update)

### 输入检查清单

- [ ] 代码仓库路径已提供
- [ ] 支持的语言：Java、Python、TypeScript
- [ ] 已有 product context（可选，用于规则匹配）

### 执行步骤

#### Step 0: 代码扫描

**扫描目标（按优先级）**:

1. **领域层（Domain Layer）**
   - Entity/Model 类
   - Domain Service
   - 状态机定义

2. **应用层（Application Layer）**
   - Service/UseCase
   - 权限注解
   - 校验逻辑

3. **接口层（Interface Layer）**
   - Controller
   - API 定义

4. **配置层**
   - application.yml
   - 数据库配置
   - 中间件配置

#### Step 1: 业务规则提取

**提取类型**:

| 规则类型 | 扫描位置 | 提取方式 |
|---------|---------|---------|
| 权限规则 | Controller、Service | 注解 + 条件判断 |
| 状态规则 | Entity、StateMachine | 状态转换方法 |
| 前置条件 | Service 方法入口 | 参数校验 |
| 后置条件 | Service 方法出口 | 字段赋值 |
| 数据校验 | DTO/Request 类 | 校验注解 |
| 业务约束 | Service 方法 | 计数/限流逻辑 |

#### Step 2: 规则匹配与映射

如果已有产品上下文数据库：

1. **查询产品规则**
   ```sql
   SELECT * FROM entities 
   WHERE domain = 'product' AND type = 'rule';
   ```

2. **匹配算法**
   - 关键词匹配（规则名称相似度）
   - 语义匹配（规则内容相似度）
   - 上下文匹配（所属模块关联）

3. **建立关系**
   - 匹配成功 → validates 关系
   - 无匹配 → orphan 标记
   - 冲突 → conflicts 标记

### 输出检查清单

- [ ] code-rules-YYYY-MM-DD.md 已生成
- [ ] rule-mapping-report.md 已生成
- [ ] orphaned-rules.md（孤儿规则列表）
- [ ] context.db 已更新代码实体
- [ ] relations 表已更新映射关系

---

## 流程 4: 一致性检查 (/context:check-consistency)

### 输入检查清单

- [ ] 已有 context.db
- [ ] 代码变更范围（--staged 或 --since）

### 执行步骤

#### Step 0: 变更规则提取

1. **获取变更文件列表**
   ```bash
   git diff --name-only {since}..{to}
   ```

2. **提取变更前后规则**
   - 对变更的代码文件重新提取规则
   - 对比修改前 vs 修改后

#### Step 1: 一致性检查

**检查场景**:

| 场景 | 检测逻辑 | 输出 |
|------|---------|------|
| 规则冲突 | 新代码规则与产品规则矛盾 | ⚠️ 冲突报告 |
| 规则弱化 | 删除了原有校验逻辑 | ⚠️ 警告 |
| 规则增强 | 添加了额外约束 | ✅ 建议同步 PRD |
| 孤儿规则 | 新增代码规则无产品对应 | ℹ️ 建议补充 |

#### Step 2: 产品影响分析

**分析维度**:

1. **功能影响**
   - 直接影响：变更代码实现的功能
   - 间接影响：依赖该代码的功能

2. **用户场景影响**
   - 受影响的角色
   - 受影响的业务流程

3. **依赖功能影响**
   - 下游功能
   - 关联模块

4. **测试覆盖建议**
   - 需测试的新场景
   - 回归测试范围

### 输出检查清单

- [ ] consistency-check-report.md 已生成
- [ ] impact-analysis-report.md 已生成
- [ ] 冲突列表（如有）
- [ ] 警告列表（如有）
- [ ] 建议操作列表

---

## 通用检查清单

### 数据库完整性检查

```sql
-- 检查实体数量
SELECT domain, type, COUNT(*) FROM entities GROUP BY domain, type;

-- 检查孤儿规则
SELECT * FROM relations WHERE relation_type = 'orphan';

-- 检查冲突
SELECT * FROM relations WHERE relation_type = 'conflicts';

-- 检查版本历史
SELECT * FROM versions ORDER BY date;
```

### 输出文件命名规范

| 文件类型 | 命名格式 | 示例 |
|---------|---------|------|
| 产品上下文 | product-context-YYYY-MM-DD.md | product-context-2026-04-09.md |
| 代码规则 | code-rules-YYYY-MM-DD.md | code-rules-2026-04-09.md |
| 规则映射 | rule-mapping-report.md | rule-mapping-report.md |
| 冲突报告 | conflict-report-YYYY-MM-DD.md | conflict-report-2026-04-09.md |
| 影响分析 | impact-analysis-YYYY-MM-DD.md | impact-analysis-2026-04-09.md |
| 孤儿规则 | orphaned-rules-YYYY-MM-DD.md | orphaned-rules-2026-04-09.md |

### 质量检查

- [ ] 所有实体都有有效的 ID
- [ ] 所有实体都有 source_file 记录
- [ ] 关系表的 from_entity 和 to_entity 都存在
- [ ] 版本链完整（parent_iteration 有效）
- [ ] 输出文档格式正确，Markdown 渲染正常
