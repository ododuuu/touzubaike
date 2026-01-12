
import argparse
import sys
import os
import json
import time
from typing import Optional

# Import Skills
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from skills.crawler import run_crawler
from skills.analyzer import run_analyzer
from skills.outliner import generate_outline
from skills.writer import write_section
from skills.reviewer import review_draft
from skills.reviser import revise_draft
from skills.deployer import deploy_to_git
from state import ArticleState, MasterOutline, CompetitorAnalysis

STATE_FILE = "article_state.json"

def save_state(state: ArticleState):
    # Quick and dirty serialization
    # In production, use a proper serializer (marshmallow/pydantic)
    # Here we just dump what we can, realizing dataclasses aren't directly JSON serializable by default
    # without helper. We'll implement a simple dict converter or pickle it.
    # For now, let's just pickle it to be safe and fast.
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
    
    # 1. Search (Mocking search results for now, or use a search API)
    # In a real agent, we'd use a Search Skill (SerpApi etc).
    # Here we will hardcode the top URLs we found earlier for "Taiwan Exchange" as a demo
    # Or rely on user input. For automation, let's assume we have a list.
    if "台灣虛擬貨幣交易所" in keyword:
        target_urls = [
            "https://max.maicoin.com/",
            "https://www.bitopro.com/", 
            "https://xrex.io/"
            # Add competitor articles here in reality
        ]
    else:
        target_urls = []
        print("Warning: No specific URLs defined for this keyword. Research might be empty.")

    # 2. Crawl
    pages = run_crawler(target_urls)
    
    # 3. Analyze
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

    # Generate Outline
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

    # Loop through sections
    total_sections = len(state.outline.sections)
    
    for i, section in enumerate(state.outline.sections):
        if section.status == "approved":
            print(f"Skipping {section.h2_title} (Already Approved)")
            continue
            
        print(f"\n[{i+1}/{total_sections}] Writing: {section.h2_title}...")
        
        # 1. Draft
        draft = write_section(section)
        # print(f"Draft generated ({len(draft)} chars). Reviewing...")
        
        # 2. Review Loop
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
        
        # Save state after every section to avoid data loss
        save_state(state)

    print("\nWriting complete.")

def cmd_assemble_and_deploy():
    print("--- Stage 4: Deploying ---")
    state = load_state()
    if not state or not state.outline:
        print("Error: State not ready.")
        return

    # Assemble Markdown
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
            # Fix heading levels: H1 -> H2, H2 -> H3, etc.
            fixed_content = sec.draft_content
            # Replace lines starting with '# ' (H1) with '## ' (H2)
            lines = fixed_content.split('\n')
            fixed_lines = []
            for line in lines:
                if line.startswith('# '):
                    fixed_lines.append('##' + line[1:])  # # Title -> ## Title
                else:
                    fixed_lines.append(line)
            fixed_content = '\n'.join(fixed_lines)
            content.append(fixed_content)
            content.append("\n---\n")
    
    final_md = "\n".join(content)
    
    # Generate a clean English slug from the keyword
    # Mapping common Chinese keywords to English slugs
    slug_map = {
        "幣安 Binance 教學": "binance-tutorial",
        "台灣虛擬貨幣交易所評比": "taiwan-crypto-exchange-comparison",
        "MAX 交易所教學": "max-exchange-guide",
        "USDT 是什麼": "what-is-usdt",
        "加密貨幣入門": "crypto-beginner-guide",
    }
    
    # Try to find a predefined slug, otherwise use a slugified version
    slug = slug_map.get(state.keyword, None)
    if not slug:
        # Fallback: create a simple slug from English words or numbers in keyword
        import re
        english_parts = re.findall(r'[a-zA-Z0-9]+', state.keyword)
        if english_parts:
            slug = '-'.join(english_parts).lower()
        else:
            # Last resort: use a simple hash
            slug = f"article-{abs(hash(state.keyword)) % 10000}"
    
    filename = f"{slug}.md"
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../src/content/blog", filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(final_md)
        
    print(f"File written to: {filepath}")
    
    # Git Deploy
    deploy_to_git(filepath, f"Auto-generated article for {state.keyword}")

def main():
    parser = argparse.ArgumentParser(description="Deep SEO Agent CLI")
    parser.add_argument("command", choices=["research", "plan", "write", "deploy"], help="Stage to execute")
    parser.add_argument("--keyword", help="Target keyword for research stage")
    
    args = parser.parse_args()
    
    if args.command == "research":
        if not args.keyword:
            print("Error: --keyword required for research")
            return
        cmd_research(args.keyword)
    elif args.command == "plan":
        cmd_plan()
    elif args.command == "write":
        cmd_write()
    elif args.command == "deploy":
        cmd_assemble_and_deploy()

if __name__ == "__main__":
    main()
