#!/bin/bash
# 每日进度更新脚本
# 运行时间: 每天 08:00

PROJECT_DIR="/Users/nealchan/clawd/projects"
TODO_FILE="/Users/nealchan/clawd/TODO.md"
REPORT_FILE="/Users/nealchan/clawd/DAILY_REPORT.md"

echo "=== 每日项目进度更新 ==="
echo "时间: $(date)"
echo ""

# 生成报告头部
cat > "$REPORT_FILE" << EOF
# 每日项目报告

**生成时间**: $(date '+%Y-%m-%d %H:%M')

## 项目状态摘要

| 项目 | 进度 | 状态 | 最后更新 |
|------|------|------|----------|
EOF

# 扫描所有项目
for project_path in "$PROJECT_DIR"/*/; do
    if [ -d "$project_path" ]; then
        project_name=$(basename "$project_path")
        progress_file="$project_path/progress.md"
        
        if [ -f "$progress_file" ]; then
            # 提取进度（从 "整体进度" 行）
            progress=$(grep -oP "整体进度.*?(\d+)" "$progress_file" | grep -oP "\d+" || echo "?")
            
            # 提取状态（从 emoji）
            if grep -q "🔴 未开始" "$progress_file"; then
                status="🔴 未开始"
            elif grep -q "🟡 进行中" "$progress_file"; then
                status="🟡 进行中"
            elif grep -q "🟢 已完成" "$progress_file"; then
                status="🟢 已完成"
            else
                status="⚪ 未知"
            fi
            
            # 提取最后更新时间
            last_update=$(stat -f %Sm "$progress_file" 2>/dev/null || echo "未知")
            
            echo "| $project_name | ${progress}% | $status | $last_update |" >> "$REPORT_FILE"
        fi
    fi
done

# 添加 todo 统计
echo "" >> "$REPORT_FILE"
echo "## 待办统计" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

total_tasks=0
completed_tasks=0

for project_path in "$PROJECT_DIR"/*/; do
    if [ -d "$project_path" ]; then
        progress_file="$project_path/progress.md"
        if [ -f "$progress_file" ]; then
            project_tasks=$(grep -c "^\s*- \[ \]" "$progress_file" 2>/dev/null || echo 0)
            project_done=$(grep -c "^\s*- \[x\]" "$progress_file" 2>/dev/null || echo 0)
            total_tasks=$((total_tasks + project_tasks + project_done))
            completed_tasks=$((completed_tasks + project_done))
        fi
    fi
done

echo "- 总任务数: $total_tasks" >> "$REPORT_FILE"
echo "- 已完成: $completed_tasks" >> "$REPORT_FILE"
echo "- 待完成: $((total_tasks - completed_tasks))" >> "$REPORT_FILE"

if [ $total_tasks -gt 0 ]; then
    completion_rate=$((completed_tasks * 100 / total_tasks))
    echo "- 完成率: ${completion_rate}%" >> "$REPORT_FILE"
fi

echo "✅ 报告已生成: $REPORT_FILE"
