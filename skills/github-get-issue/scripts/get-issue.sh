#!/bin/bash
# GitHub Issue 查询脚本 - 获取单个 issue 详情
# 用法: ./scripts/get-issue.sh <issue-number>

ISSUE_NUMBER="$1"

# 验证参数
if [ -z "$ISSUE_NUMBER" ]; then
  echo "❌ 错误: 请提供 issue 编号"
  echo "用法: ./scripts/get-issue.sh <issue-number>"
  echo "示例: ./scripts/get-issue.sh 42"
  exit 1
fi

if ! [[ "$ISSUE_NUMBER" =~ ^[0-9]+$ ]]; then
  echo "❌ 错误: issue 编号必须是数字"
  exit 1
fi

# 检查 gh 是否安装
if ! command -v gh &> /dev/null; then
  echo "❌ 错误: GitHub CLI (gh) 未安装"
  echo "请访问 https://cli.github.com/ 安装"
  exit 1
fi

# 检查是否已登录
if ! gh auth status &> /dev/null; then
  echo "❌ 错误: GitHub CLI 未登录"
  echo "请运行: gh auth login"
  exit 1
fi

echo "🔍 正在获取 Issue #$ISSUE_NUMBER 的详情..."
echo ""

# 获取 issue 详情（JSON 格式便于解析）
ISSUE_DATA=$(gh issue view "$ISSUE_NUMBER" --json number,title,state,body,author,createdAt,updatedAt,labels,comments,url 2>&1)

if [ $? -ne 0 ]; then
  echo "❌ 无法获取 issue #$ISSUE_NUMBER"
  echo ""
  echo "可能原因:"
  echo "  • issue 不存在"
  echo "  • 没有访问权限"
  echo "  • 未登录 GitHub CLI (运行 gh auth login)"
  exit 1
fi

# 输出 JSON 格式
echo "$ISSUE_DATA"
