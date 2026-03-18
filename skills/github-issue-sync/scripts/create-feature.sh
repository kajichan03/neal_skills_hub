#!/bin/bash
# GitHub Issue Feature Request 创建脚本
# 用法: ./scripts/create-feature.sh "<标题>" "<现状>" "<问题>" "<预期>" "<优先级>" "<补充信息>"

TITLE="$1"
CURRENT="$2"
PROBLEM="$3"
EXPECTED="$4"
PRIORITY="$5"
EXTRA="$6"

# 构建 body
BODY="## 现状
$CURRENT

## 问题
$PROBLEM

## 预期
$EXPECTED

## 优先级
$PRIORITY

## 补充信息
$EXTRA"

# 创建 issue
gh issue create \
  --title "[Feature] $TITLE" \
  --body "$BODY" \
  --label "enhancement"
