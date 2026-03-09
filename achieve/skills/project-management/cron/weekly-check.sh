#!/bin/bash
# 每周结构健康检查脚本
# 运行时间: 每周一 09:00

PROJECT_DIR="/Users/nealchan/clawd/projects"
TODO_FILE="/Users/nealchan/clawd/TODO.md"
REPORT_FILE="/Users/nealchan/clawd/WEEKLY_HEALTH_REPORT.md"

echo "=== 每周项目健康检查 ==="
echo "时间: $(date)"
echo ""

issues=()

# 检查 1: 每个项目都有必需文件
echo "检查 1: 项目结构完整性..."
for project_path in "$PROJECT_DIR"/*/; do
    if [ -d "$project_path" ]; then
        project_name=$(basename "$project_path")
        
        if [ ! -f "$project_path/progress.md" ]; then
            issues+=("❌ $project_name: 缺少 progress.md")
        fi
        
        if [ ! -f "$project_path/decisions.md" ]; then
            issues+=("❌ $project_name: 缺少 decisions.md")
        fi
    fi
done

# 检查 2: 项目名称规范
echo "检查 2: 项目名称规范..."
for project_path in "$PROJECT_DIR"/*/; do
    if [ -d "$project_path" ]; then
        project_name=$(basename "$project_path")
        
        # 检查是否包含大写字母
        if [[ "$project_name" =~ [A-Z] ]]; then
            issues+=("❌ $project_name: 项目名称包含大写字母，应使用小写")
        fi
        
        # 检查是否包含空格
        if [[ "$project_name" =~ [[:space:]] ]]; then
            issues+=("❌ $project_name: 项目名称包含空格，应使用连字符")
        fi
    fi
done

# 检查 3: TODO.md 没有直接写的任务
echo "检查 3: TODO.md 规范性..."
if grep -q "^- \[ \]" "$TODO_FILE" 2>/dev/null; then
    issues+=("❌ TODO.md 包含未分类任务（直接写的 - [ ]）")
fi

# 检查 4: 孤立文件（在项目目录外）
echo "检查 4: 孤立文件检查..."
# 检查 clawd 根目录下是否有 .md 文件（应该在项目内）
for file in /Users/nealchan/clawd/*.md; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        if [[ "$filename" != "README.md" && "$filename" != "TODO.md" && "$filename" != "ARCHITECTURE.md" && "$filename" != "RETROSPECTIVE.md" && "$filename" != "MEMORY.md" && "$filename" != "HEARTBEAT.md" && "$filename" != "DAILY_REPORT.md" && "$filename" != "WEEKLY_HEALTH_REPORT.md" ]]; then
            issues+=("⚠️ 孤立文件: $filename (建议移到项目目录内)")
        fi
    fi
done

# 检查 5: 超过 30 天未更新的项目
echo "检查 5: 项目活跃度检查..."
for project_path in "$PROJECT_DIR"/*/; do
    if [ -d "$project_path" ]; then
        project_name=$(basename "$project_path")
        progress_file="$project_path/progress.md"
        
        if [ -f "$progress_file" ]; then
            # 获取最后修改时间（秒）
            last_mod=$(stat -f %m "$progress_file" 2>/dev/null)
            now=$(date +%s)
            days_since_update=$(( (now - last_mod) / 86400 ))
            
            if [ $days_since_update -gt 30 ]; then
                issues+=("⚠️ $project_name: ${days_since_update}天未更新，建议归档")
            fi
        fi
    fi
done

# 生成报告
cat > "$REPORT_FILE" << EOF
# 每周项目健康报告

**检查时间**: $(date '+%Y-%m-%d %H:%M')

## 检查结果

EOF

if [ ${#issues[@]} -eq 0 ]; then
    echo "✅ 所有检查通过！项目结构健康。" >> "$REPORT_FILE"
else
    echo "发现 ${#issues[@]} 个问题：" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    for issue in "${issues[@]}"; do
        echo "$issue" >> "$REPORT_FILE"
    done
fi

echo "" >> "$REPORT_FILE"
echo "## 统计信息" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

project_count=$(find "$PROJECT_DIR" -maxdepth 1 -type d | wc -l)
project_count=$((project_count - 1))  # 减去目录本身

echo "- 项目总数: $project_count" >> "$REPORT_FILE"
echo "- 发现问题: ${#issues[@]}" >> "$REPORT_FILE"

echo "✅ 报告已生成: $REPORT_FILE"

# 如果有严重问题，输出提醒
if [ ${#issues[@]} -gt 0 ]; then
    echo ""
    echo "⚠️ 发现 ${#issues[@]} 个问题，请查看报告并修复"
fi
