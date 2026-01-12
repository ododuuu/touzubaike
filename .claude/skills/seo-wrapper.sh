#!/bin/bash
# SEO Skill Wrapper - Claude Code to Python CLI Bridge

set -e

# 設定工作目錄
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SEO_AGENT_DIR="$PROJECT_ROOT/tools/seo_agent"

# 設定環境變數
export GEMINI_API_KEY="${GEMINI_API_KEY:-AIzaSyBEYAgOQGfl4vFEqKyy09smnsbgkAxTC_c}"

# 解析參數
ACTION="$1"
PLATFORM="$2"
FLAGS="${@:3}"

# 進入 SEO Agent 目錄
cd "$SEO_AGENT_DIR"

case "$ACTION" in
  "generate"|"gen")
    if [ -z "$PLATFORM" ]; then
      echo "❌ Error: Platform ID required"
      echo "Usage: /seo generate <platform-id>"
      echo "Example: /seo generate bitopro"
      exit 1
    fi

    echo "🚀 Generating scam prevention page for: $PLATFORM"
    echo ""
    python3 main.py scam-generate --platform "$PLATFORM" $FLAGS
    echo ""
    echo "✅ Done! View at: /blog/scam/$PLATFORM/"
    ;;

  "list"|"ls")
    echo "📋 Available platforms:"
    echo ""
    python3 main.py scam-list
    ;;

  "batch"|"all")
    echo "🔄 Batch generating all scam prevention pages..."
    echo ""
    python3 main.py scam-generate-all $FLAGS
    ;;

  "analyze"|"check")
    if [ -z "$PLATFORM" ]; then
      echo "❌ Error: Platform ID required"
      echo "Usage: /seo analyze <platform-id>"
      exit 1
    fi

    FILE_PATH="$PROJECT_ROOT/src/content/blog/scam/$PLATFORM.md"

    if [ ! -f "$FILE_PATH" ]; then
      echo "❌ Error: File not found: $FILE_PATH"
      exit 1
    fi

    echo "📊 Analyzing SEO for: $PLATFORM"
    echo ""

    # 使用 Python 進行 SEO 分析
    python3 -c "
import sys
sys.path.insert(0, '$SEO_AGENT_DIR')
from skills.seo_optimizer import SEOOptimizer
from skills.scam_data_loader import ScamDataLoader

# 讀取檔案
with open('$FILE_PATH', 'r', encoding='utf-8') as f:
    content = f.read()

# 載入 metadata
loader = ScamDataLoader()
platform = loader.get_platform('$PLATFORM')

if platform:
    metadata = {
        'title': f'{platform.chinese_name}詐騙手法大公開｜2026最新防範指南',
        'description': f'完整解析{platform.chinese_name}常見詐騙手法',
        'keywords': platform.keywords
    }

    # 分析
    optimizer = SEOOptimizer()
    result = optimizer.analyze(content, metadata)

    print(f'SEO Score: {result[\"score\"]}/100')
    print(f'Word Count: {result[\"stats\"][\"word_count\"]}')
    print(f'H2 Headings: {result[\"stats\"][\"h2_count\"]}')
    print(f'Links: {result[\"stats\"][\"link_count\"]}')
    print()

    if result['issues']:
        print('Issues:')
        for issue in result['issues']:
            icon = '❌' if issue.severity == 'error' else '⚠️' if issue.severity == 'warning' else 'ℹ️'
            print(f'  {icon} [{issue.severity}] {issue.message}')
            print(f'      → {issue.suggestion}')
    else:
        print('✅ No issues found!')
"
    ;;

  "deploy")
    echo "🚀 Deploying scam prevention pages..."
    cd "$PROJECT_ROOT"

    git add src/content/blog/scam/

    if git diff --staged --quiet; then
      echo "ℹ️  No changes to deploy"
    else
      git commit -m "Update scam prevention pages

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
      git push
      echo "✅ Deployed successfully!"
    fi
    ;;

  "help"|*)
    echo "SEO Skill - Programmatic SEO Content Generation"
    echo ""
    echo "Usage:"
    echo "  /seo generate <platform>  Generate single page"
    echo "  /seo list                 List all platforms"
    echo "  /seo batch                Generate all pages"
    echo "  /seo analyze <platform>   Analyze SEO score"
    echo "  /seo deploy               Deploy to Git"
    echo ""
    echo "Examples:"
    echo "  /seo generate bitopro"
    echo "  /seo generate usdt --dry-run"
    echo "  /seo batch"
    echo "  /seo analyze okx"
    echo ""
    echo "Available platforms:"
    python3 "$SEO_AGENT_DIR/main.py" scam-list 2>/dev/null | grep -E '^\s+\w+' | head -5
    echo "  ..."
    ;;
esac
