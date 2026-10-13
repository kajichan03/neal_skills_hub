# Context Portal 数据模型

> 详细的 SQLite Schema 定义和实体类型说明

---

## 核心表结构

### 1. entities 表 - 统一实体存储

```sql
CREATE TABLE entities (
    id TEXT PRIMARY KEY,              -- 实体唯一标识
    name TEXT NOT NULL,               -- 实体名称
    domain TEXT NOT NULL,             -- 领域：product | code
    type TEXT NOT NULL,               -- 类型（根据 domain 不同）
    content TEXT NOT NULL,            -- 完整内容（Markdown/JSON）
    content_hash TEXT,                -- 内容哈希（用于快速比对）
    token_count INTEGER,              -- Token 数（用于检索时控制）
    
    -- 来源信息
    source_file TEXT,                 -- 来源文件路径
    source_type TEXT,                 -- 来源类型：prd | openapi | config | commit
    iteration_id TEXT,                -- 迭代标识（如：Sprint-24）
    
    -- 时间戳
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE INDEX idx_entities_domain ON entities(domain);
CREATE INDEX idx_entities_type ON entities(type);
CREATE INDEX idx_entities_iteration ON entities(iteration_id);
CREATE INDEX idx_entities_updated ON entities(updated_at);
CREATE INDEX idx_entities_domain_type ON entities(domain, type);
```

**实体类型定义**:

| domain | type | 说明 | 示例 |
|--------|------|------|------|
| product | module | 产品功能模块 | 工单中心、变更管理 |
| product | feature | 具体功能点 | 工单列表、审批流程 |
| product | rule | 业务规则 | 审批权限规则、状态流转规则 |
| product | persona | 用户角色 | 安全工程师、审批人 |
| product | state | 状态定义 | 待审批、已批准、已完成 |
| product | permission | 权限规则 | 角色可见性、可操作性 |
| **product** | **ticket_type** | **工单类型** | **泳道新建、业务系统申请** |
| **product** | **approval_flow** | **审批流程** | **业务系统申请审批流程** |
| **product** | **approval_node** | **审批节点** | **业务系统owner并签** |
| **product** | **form_field** | **表单字段** | **工单标题、业务系统名称** |
| **product** | **notification** | **通知模板** | **待执行邮件通知** |
| **product** | **derived_process** | **派生流程** | **证书申请派生工单** |
| **product** | **page** | **页面** | **工单列表页、详情页** |
| **product** | **page_structure** | **页面结构** | **页面布局、组件层级** |
| code | service | 微服务 | ticket-service |
| code | api | 接口 | POST /api/v1/tickets |
| code | model | 数据模型 | Ticket、ChangeRequest |
| code | config | 配置项 | database.url |

---

### 2. relations 表 - 关系存储

```sql
CREATE TABLE relations (
    id TEXT PRIMARY KEY,
    from_entity TEXT NOT NULL,        -- 源实体 ID
    from_domain TEXT NOT NULL,        -- 源实体领域
    to_entity TEXT NOT NULL,          -- 目标实体 ID
    to_domain TEXT NOT NULL,          -- 目标实体领域
    relation_type TEXT NOT NULL,      -- 关系类型
    
    -- 元数据
    iteration_id TEXT,
    confidence REAL DEFAULT 1.0,      -- 置信度（0-1）
    is_cross_domain BOOLEAN,          -- 是否跨域关联
    metadata TEXT,                    -- 额外信息（JSON）
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (from_entity) REFERENCES entities(id),
    FOREIGN KEY (to_entity) REFERENCES entities(id)
);

-- 索引
CREATE INDEX idx_relations_from ON relations(from_entity);
CREATE INDEX idx_relations_to ON relations(to_entity);
CREATE INDEX idx_relations_type ON relations(relation_type);
CREATE INDEX idx_relations_cross ON relations(is_cross_domain);
```

**关系类型定义**:

| 类型 | 适用场景 | 示例 |
|------|---------|------|
| contains | 同域：包含关系 | 工单中心 contains 工单列表 |
| depends_on | 同域：依赖关系 | ticket-service depends_on user-service |
| references | 同域：引用关系 | 工单列表页 references Ticket |
| **has_ticket_type** | **模块包含工单类型** | **工单中心 has_ticket_type 泳道新建** |
| **has_approval_flow** | **工单类型包含审批流程** | **业务系统申请 has_approval_flow 5节点审批** |
| **has_form_field** | **工单类型包含表单字段** | **泳道新建 has_form_field 泳道名称** |
| **has_notification** | **状态包含通知模板** | **待执行 has_notification 邮件通知** |
| **has_derived_process** | **工单类型包含派生流程** | **业务系统变更 has_derived_process 证书申请** |
| **has_page** | **模块包含页面** | **工单中心 has_page 工单列表页** |
| implements | 跨域：功能实现 | 工单中心 implements ticket-service |
| exposes | 跨域：暴露接口 | 工单中心 exposes POST /api/v1/tickets |
| uses | 跨域：使用模型 | 创建工单页面 uses Ticket |
| validates | 跨域：验证规则 | 代码规则 validates 产品规则 |
| conflicts | 跨域：规则冲突 | 代码规则 conflicts 产品规则 |
| orphan | 跨域：孤儿规则 | 代码规则 orphan（无对应产品规则） |

---

### 3. versions 表 - 版本历史

```sql
CREATE TABLE versions (
    iteration_id TEXT PRIMARY KEY,    -- 迭代标识
    date DATE NOT NULL,               -- 日期
    summary TEXT,                     -- 变更摘要
    entity_count INTEGER,             -- 实体数量
    
    -- 版本链（支持追溯）
    parent_iteration TEXT,            -- 父版本
    
    -- 快照
    snapshot_path TEXT,               -- 完整上下文文件路径
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (parent_iteration) REFERENCES versions(iteration_id)
);
```

---

### 4. chunks 表 - 文本分块（用于检索）

```sql
CREATE TABLE chunks (
    id TEXT PRIMARY KEY,
    entity_id TEXT NOT NULL,          -- 所属实体
    content TEXT NOT NULL,            -- 分块内容
    chunk_type TEXT,                  -- 类型：summary | detail | rule
    
    -- 位置信息
    start_line INTEGER,
    end_line INTEGER,
    token_count INTEGER,
    
    FOREIGN KEY (entity_id) REFERENCES entities(id)
);

-- FTS5 全文搜索虚拟表
CREATE VIRTUAL TABLE chunks_fts USING fts5(
    content,
    content='chunks',
    content_rowid='rowid'
);
```

---

## 实体 ID 命名规范

### Product Domain

```
module:{模块名}
  示例: module:工单中心

feature:{模块名}:{功能点名}
  示例: feature:工单中心:工单列表

rule:{模块名}:{规则名}
  示例: rule:工单中心:审批权限

persona:{角色名}
  示例: persona:安全工程师

page:{页面名}
  示例: page:工单列表页

# 新增类型
ticket_type:{工单类型名}
  示例: ticket_type:泳道新建

approval_flow:{工单类型名}:flow
  示例: approval_flow:业务系统申请:flow

approval_node:{工单类型名}:node{序号}
  示例: approval_flow:业务系统申请:node1

form_field:{工单类型名}:{字段名}
  示例: form_field:泳道新建:泳道名称

notification:{触发状态}:notification
  示例: notification:待执行:notification

derived_process:{父工单类型}:{派生类型}
  示例: derived_process:业务系统变更:证书申请

page_structure:{页面名}:structure
  示例: page_structure:工单列表页:structure
```

### Code Domain

```
service:{服务名}
  示例: service:ticket-service

api:{服务名}:{方法}:{路径}
  示例: api:ticket-service:POST:/api/v1/tickets

model:{服务名}:{模型名}
  示例: model:ticket-service:Ticket

config:{服务名}:{配置项}
  示例: config:ticket-service:database.url
```

---

## 跨域关联示例

```
产品实体                              代码实体
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
module:工单中心 ──implements──► service:ticket-service
     │                               │
     ├─has_ticket_type──► ticket_type:泳道新建
     │                          │
     │                          ├─has_approval_flow──► approval_flow:泳道新建:flow
     │                          │                           │
     │                          │                           ├─contains──► approval_node:泳道新建:node1
     │                          │                           └─contains──► approval_node:泳道新建:node2
     │                          │
     │                          ├─has_form_field──► form_field:泳道新建:泳道名称
     │                          ├─has_form_field──► form_field:泳道新建:泳道负责人
     │                          │
     │                          └─has_derived_process──► derived_process:泳道新建:中间件创建
     │
     ├─has_page──► page:工单列表页
     │                 │
     │                 └─has_structure──► page_structure:工单列表页:structure
     │
     ├─exposes──► api:ticket-service:POST:/api/v1/tickets
     │
     └─uses────► model:ticket-service:Ticket

rule:工单中心:审批权限 ──validates──► code:Ticket.java:approve()
```

---

## 查询示例

### 查询产品所有功能模块

```sql
SELECT * FROM entities 
WHERE domain = 'product' AND type = 'module';
```

### 查询服务的所有 API

```sql
SELECT * FROM entities 
WHERE domain = 'code' AND type = 'api' 
AND source_file LIKE '%ticket-service%';
```

### 查询功能的实现服务

```sql
SELECT e.* FROM entities e
JOIN relations r ON e.id = r.to_entity
WHERE r.from_entity = 'module:工单中心'
AND r.relation_type = 'implements';
```

### 查询工单类型的审批流程

```sql
SELECT e.* FROM entities e
JOIN relations r ON e.id = r.to_entity
WHERE r.from_entity = 'ticket_type:泳道新建'
AND r.relation_type = 'has_approval_flow';
```

### 查询工单类型的表单字段

```sql
SELECT e.* FROM entities e
JOIN relations r ON e.id = r.to_entity
WHERE r.from_entity = 'ticket_type:泳道新建'
AND r.relation_type = 'has_form_field'
ORDER BY e.content->>'order';
```

### 查询规则冲突

```sql
SELECT * FROM relations 
WHERE relation_type = 'conflicts';
```

### 全文搜索

```sql
SELECT c.*, e.name, e.type 
FROM chunks_fts fts
JOIN chunks c ON fts.rowid = c.rowid
JOIN entities e ON c.entity_id = e.id
WHERE chunks_fts MATCH '审批权限';
```

---

## 产品经理使用场景查询

### 查询某个工单类型的完整信息

```sql
-- 获取工单类型基本信息
SELECT * FROM entities WHERE id = 'ticket_type:泳道新建';

-- 获取审批流程
SELECT af.*, an.content as node_content
FROM entities af
JOIN relations r ON af.id = r.from_entity
JOIN entities an ON r.to_entity = an.id
WHERE af.id = 'approval_flow:泳道新建:flow'
AND r.relation_type = 'contains'
ORDER BY an.content->>'sequence';

-- 获取表单字段
SELECT f.* FROM entities f
JOIN relations r ON f.id = r.to_entity
WHERE r.from_entity = 'ticket_type:泳道新建'
AND r.relation_type = 'has_form_field'
ORDER BY f.content->>'order';

-- 获取派生流程
SELECT dp.* FROM entities dp
JOIN relations r ON dp.id = r.to_entity
WHERE r.from_entity = 'ticket_type:泳道新建'
AND r.relation_type = 'has_derived_process';

-- 获取通知模板
SELECT n.* FROM entities n
JOIN relations r ON n.id = r.to_entity
WHERE r.from_entity = 'ticket_type:泳道新建'
AND r.relation_type = 'has_notification';
```

### 查询某个页面的完整结构

```sql
SELECT ps.* FROM entities ps
JOIN relations r ON ps.id = r.to_entity
WHERE r.from_entity = 'page:工单列表页'
AND r.relation_type = 'has_structure';
```
