#!/bin/bash
# GitHub Issue Bug 创建脚本
# 用法: ./scripts/create-bug.sh "<标题>" "<问题描述>" "<复现步骤>" "<期望结果>" "<实际结果>" "<环境信息>" "<错误日志>"

TITLE="$1"
DESCRIPTION="$2"
REPRO_STEPS="$3"
EXPECTED="$4"
ACTUAL="$5"
ENVIRONMENT="$6"
LOGS="$7"

# 构建 body
BODY="## 问题描述
$DESCRIPTION

## 复现步骤
$REPRO_STEPS

## 期望结果
$EXPECTED

## 实际结果
$ACTUAL

## 环境信息
$ENVIRONMENT

## 错误日志
<details>
<summary>展开查看</summary>

\`\`\`
$LOGS
\`\`\`
</details>"

# 创建 issue
gh issue create \
  --title "[Bug] $TITLE" \
  --body "$BODY" \
  --label "bug"
