#!/bin/bash
# GitHub Issue 查询脚本 - 获取单个 issue 详情
# 用法: ./scripts/get-issue.sh <issue-number>

ISSUE_NUMBER="$1"

if [ -z "$ISSUE_NUMBER" ]; then
  echo "错误: 请提供 issue 编号"
  echo "用法: ./scripts/get-issue.sh <issue-number>"
  exit 1
fi

# 检查是否为数字
if ! [[ "$ISSUE_NUMBER" =~ ^[0-9]+$ ]]; then
  echo "错误: issue 编号必须是数字"
  exit 1
fi

echo "=== GitHub Issue #$ISSUE_NUMBER ==="
echo ""

# 获取 issue 详情（JSON 格式便于解析）
gh issue view "$ISSUE_NUMBER" --json number,title,state,body,author,createdAt,updatedAt,labels,comments,url 2>/dev/null || {
  echo "错误: 无法获取 issue #$ISSUE_NUMBER"
  echo "可能原因:"
  echo "  - issue 不存在"
  echo "  - 没有访问权限"
  echo "  - 未登录 GitHub CLI (运行 gh auth login)"
  exit 1
}
