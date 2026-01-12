"""
SEO Agent CLI - Programmatic SEO 內容生成系統
支援傳統長文生成和批量模板生成兩種模式
"""

import argparse
import sys
import os
import json
import time
from typing import Optional, List

# Import Skills
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 原有 Skills
from skills.crawler import run_crawler
from skills.analyzer import run_analyzer
from skills.outliner import generate_outline
from skills.writer import write_section
from skills.reviewer import review_draft
from skills.reviser import revise_draft
from skills.deployer import deploy_to_git

# 新增 Programmatic SEO Skills
from skills.scam_data_loader import ScamDataLoader
from skills.scam_template_renderer import ScamTemplateRenderer
from skills.scam_content_enricher import ScamContentEnricher
from skills.seo_optimizer import SEOOptimizer

from state import ArticleState, MasterOutline, CompetitorAnalysis

STATE_FILE = "article_state.json"

# ============================================
# 原有功能（傳統長文生成）
# ============================================

def save_state(state: ArticleState):
    import pickle
    with open(STATE_FILE, "wb") as f:
        pickle.dump(state, f)
    print(f"State saved to {STATE_FILE}")

def load_state() -> Optional[ArticleState]:
    if not os.path.exists(STATE_FILE):
        return None
    import pickle
    with open(STATE_FILE, "rb") as f:
        return pickle.load(f)

def cmd_research(keyword: str):
    print(f"--- Stage 1: Researching '{keyword}' ---")

    if "台灣虛擬貨幣交易所" in keyword:
        target_urls = [
            "https://max.maicoin.com/",
            "https://www.bitopro.com/",
            "https://xrex.io/"
        ]
    else:
        target_urls = []
        print("Warning: No specific URLs defined for this keyword. Research might be empty.")

    pages = run_crawler(target_urls)
    analysis = run_analyzer(pages)

    state = ArticleState(keyword=keyword, research_data=analysis, status="planning")
    save_state(state)
    print("Research complete. Data saved.")

def cmd_plan():
    print("--- Stage 2: Planning ---")
    state = load_state()
    if not state or not state.research_data:
        print("Error: No research data found. Run 'research' first.")
        return

    print("Generating Master Outline (this may take a moment)...")
    outline = generate_outline(state.keyword, state.research_data)

    if outline:
        state.outline = outline
        state.status = "planned"
        save_state(state)
        print("\n=== Generated Outline ===")
        print(f"Title: {outline.title}")
        print(f"Sections: {len(outline.sections)}")
        for sec in outline.sections:
            print(f"  [{sec.id}] {sec.h2_title} ({sec.target_length} words)")
        print("\nReview the outline. If good, run 'write'.")
    else:
        print("Error: Failed to generate outline.")

def cmd_write():
    print("--- Stage 3: Writing ---")
    state = load_state()
    if not state or not state.outline:
        print("Error: No outline found. Run 'plan' first.")
        return

    total_sections = len(state.outline.sections)

    for i, section in enumerate(state.outline.sections):
        if section.status == "approved":
            print(f"Skipping {section.h2_title} (Already Approved)")
            continue

        print(f"\n[{i+1}/{total_sections}] Writing: {section.h2_title}...")

        draft = write_section(section)

        max_retries = 2
        current_draft = draft
        for attempt in range(max_retries + 1):
            score, feedback = review_draft(current_draft, state.keyword)
            print(f"  - Review Score: {score}/100")

            if score >= 80:
                print("  - Passed!")
                section.draft_content = current_draft
                section.status = "approved"
                section.review_score = score
                break
            else:
                print(f"  - Failed. Feedback: {feedback}")
                if attempt < max_retries:
                    print("  - Revising...")
                    current_draft = revise_draft(current_draft, feedback)
                else:
                    print("  - Max retries reached. Saving as is (needs manual check).")
                    section.draft_content = current_draft
                    section.status = "review_needed"

        save_state(state)

    print("\nWriting complete.")

def cmd_assemble_and_deploy():
    print("--- Stage 4: Deploying ---")
    state = load_state()
    if not state or not state.outline:
        print("Error: State not ready.")
        return

    content = []
    content.append("---")
    content.append(f"title: \"{state.outline.title}\"")
    content.append(f"description: \"{state.outline.description}\"")
    content.append(f"pubDate: \"{time.strftime('%Y-%m-%d')}\"")
    content.append(f"tags: [\"{state.keyword}\"]")
    content.append("---")
    content.append("")

    for sec in state.outline.sections:
        if sec.draft_content:
            fixed_content = sec.draft_content
            lines = fixed_content.split('\n')
            fixed_lines = []
            for line in lines:
                if line.startswith('# '):
                    fixed_lines.append('##' + line[1:])
                else:
                    fixed_lines.append(line)
            fixed_content = '\n'.join(fixed_lines)
            content.append(fixed_content)
            content.append("\n---\n")

    final_md = "\n".join(content)

    slug_map = {
        "幣安 Binance 教學": "binance-tutorial",
        "台灣虛擬貨幣交易所評比": "taiwan-crypto-exchange-comparison",
        "MAX 交易所教學": "max-exchange-guide",
        "USDT 是什麼": "what-is-usdt",
        "加密貨幣入門": "crypto-beginner-guide",
    }

    slug = slug_map.get(state.keyword, None)
    if not slug:
        import re
        english_parts = re.findall(r'[a-zA-Z0-9]+', state.keyword)
        if english_parts:
            slug = '-'.join(english_parts).lower()
        else:
            slug = f"article-{abs(hash(state.keyword)) % 10000}"

    filename = f"{slug}.md"
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../src/content/blog", filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(final_md)

    print(f"File written to: {filepath}")
    deploy_to_git(filepath, f"Auto-generated article for {state.keyword}")


# ============================================
# 新功能：Programmatic SEO（詐騙防範系列）
# ============================================

def cmd_scam_list():
    """列出所有可用的詐騙平台 ID"""
    print("=== 可用的詐騙平台 ID ===\n")
    loader = ScamDataLoader()

    for platform in loader.get_all_platforms():
        licensed = "✓" if platform.taiwan_licensed else "✗"
        legit = "合法" if platform.is_legit else "詐騙模式"
        print(f"  {platform.id:20} | {platform.chinese_name:15} | {legit:8} | 台灣牌照: {licensed}")

    print(f"\n共 {len(loader.get_platform_ids())} 個平台")
    print("\n使用方式: python3 main.py scam-generate --platform bitopro")


def cmd_scam_generate(platform_id: str, dry_run: bool = False):
    """生成單一詐騙防範頁面"""
    print(f"=== 生成詐騙防範頁面: {platform_id} ===\n")

    # 1. 渲染模板
    print("[1/4] 渲染模板...")
    renderer = ScamTemplateRenderer()
    try:
        rendered = renderer.render(platform_id)
    except ValueError as e:
        print(f"Error: {e}")
        print("使用 'python3 main.py scam-list' 查看可用的平台 ID")
        return

    print(f"      標題: {rendered['metadata']['title']}")
    print(f"      需要 LLM 填充的區塊: {rendered['placeholders']}")

    # 2. LLM 豐富化
    print("\n[2/4] LLM 內容豐富化...")
    enricher = ScamContentEnricher()
    enriched_content = enricher.enrich(rendered)
    print("      完成")

    # 3. SEO 優化檢查
    print("\n[3/4] SEO 優化檢查...")
    optimizer = SEOOptimizer()
    seo_result = optimizer.analyze(enriched_content, rendered['metadata'])

    print(f"      SEO 分數: {seo_result['score']}/100")
    print(f"      字數: {seo_result['stats']['word_count']}")
    print(f"      H2 標題: {seo_result['stats']['h2_count']}")

    if seo_result['issues']:
        print("      問題:")
        for issue in seo_result['issues'][:3]:
            print(f"        - [{issue.severity}] {issue.message}")

    # 4. 儲存檔案
    if dry_run:
        print("\n[4/4] Dry run 模式 - 不儲存檔案")
        print("\n=== 預覽（前 1500 字）===")
        print(enriched_content[:1500])
        return

    print("\n[4/4] 儲存檔案...")

    # 確定輸出路徑
    blog_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../src/content/blog/scam")
    os.makedirs(blog_dir, exist_ok=True)

    filename = f"{platform_id}.md"
    filepath = os.path.join(blog_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(enriched_content)

    print(f"      檔案已儲存: {filepath}")

    # 統計
    print("\n=== 完成 ===")
    print(f"平台: {rendered['metadata']['platform_name']}")
    print(f"標題: {rendered['metadata']['title']}")
    print(f"URL: /blog/scam/{platform_id}/")
    print(f"SEO 分數: {seo_result['score']}/100")


def cmd_scam_generate_all(dry_run: bool = False):
    """批量生成所有詐騙防範頁面"""
    print("=== 批量生成詐騙防範頁面 ===\n")

    loader = ScamDataLoader()
    platform_ids = loader.get_platform_ids()

    print(f"將生成 {len(platform_ids)} 個頁面\n")

    success = 0
    failed = 0

    for i, pid in enumerate(platform_ids, 1):
        print(f"\n--- [{i}/{len(platform_ids)}] {pid} ---")
        try:
            cmd_scam_generate(pid, dry_run=dry_run)
            success += 1
        except Exception as e:
            print(f"Error: {e}")
            failed += 1

        # 避免 API rate limit
        if not dry_run:
            time.sleep(2)

    print(f"\n=== 批量生成完成 ===")
    print(f"成功: {success}")
    print(f"失敗: {failed}")


def cmd_scam_deploy():
    """部署詐騙防範頁面到 Git"""
    print("=== 部署詐騙防範頁面 ===\n")

    blog_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../src/content/blog/scam")

    if not os.path.exists(blog_dir):
        print("Error: 沒有找到詐騙防範頁面目錄")
        return

    files = [f for f in os.listdir(blog_dir) if f.endswith('.md')]
    print(f"找到 {len(files)} 個檔案")

    # Git add all
    import subprocess
    try:
        subprocess.run(["git", "add", blog_dir], check=True, cwd=os.path.dirname(blog_dir))
        subprocess.run(["git", "commit", "-m", f"Add {len(files)} scam prevention guides"], check=True, cwd=os.path.dirname(blog_dir))
        print("Git commit 完成")
        print("\n請手動執行 'git push' 推送到遠端")
    except subprocess.CalledProcessError as e:
        print(f"Git 操作失敗: {e}")


# ============================================
# CLI 入口
# ============================================

def main():
    parser = argparse.ArgumentParser(
        description="SEO Agent CLI - Programmatic SEO 內容生成系統",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # 傳統長文生成
  python3 main.py research --keyword "台灣虛擬貨幣交易所評比"
  python3 main.py plan
  python3 main.py write
  python3 main.py deploy

  # Programmatic SEO: 詐騙防範系列
  python3 main.py scam-list                          # 列出所有平台
  python3 main.py scam-generate --platform bitopro   # 生成單一頁面
  python3 main.py scam-generate --platform bitopro --dry-run  # 預覽不儲存
  python3 main.py scam-generate-all                  # 批量生成所有
  python3 main.py scam-deploy                        # 部署到 Git
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="可用指令")

    # 原有指令
    research_parser = subparsers.add_parser("research", help="研究競爭對手")
    research_parser.add_argument("--keyword", required=True, help="目標關鍵詞")

    subparsers.add_parser("plan", help="生成大綱")
    subparsers.add_parser("write", help="撰寫全文")
    subparsers.add_parser("deploy", help="部署文章")

    # 新增指令：詐騙防範系列
    subparsers.add_parser("scam-list", help="列出所有詐騙平台 ID")

    scam_gen_parser = subparsers.add_parser("scam-generate", help="生成詐騙防範頁面")
    scam_gen_parser.add_argument("--platform", required=True, help="平台 ID（如 bitopro, usdt）")
    scam_gen_parser.add_argument("--dry-run", action="store_true", help="預覽模式，不儲存檔案")

    scam_all_parser = subparsers.add_parser("scam-generate-all", help="批量生成所有詐騙防範頁面")
    scam_all_parser.add_argument("--dry-run", action="store_true", help="預覽模式，不儲存檔案")

    subparsers.add_parser("scam-deploy", help="部署詐騙防範頁面到 Git")

    args = parser.parse_args()

    if args.command == "research":
        cmd_research(args.keyword)
    elif args.command == "plan":
        cmd_plan()
    elif args.command == "write":
        cmd_write()
    elif args.command == "deploy":
        cmd_assemble_and_deploy()
    elif args.command == "scam-list":
        cmd_scam_list()
    elif args.command == "scam-generate":
        cmd_scam_generate(args.platform, dry_run=args.dry_run)
    elif args.command == "scam-generate-all":
        cmd_scam_generate_all(dry_run=args.dry_run)
    elif args.command == "scam-deploy":
        cmd_scam_deploy()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
