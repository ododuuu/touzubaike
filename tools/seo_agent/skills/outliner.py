
import sys
import os
import json
from typing import List

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from state import CompetitorAnalysis, MasterOutline, SectionState
from skills.llm_client import call_llm, parse_json_response

PROMPT_TEMPLATE = """
你是一位專家級的 SEO 策略師。
目標：建立一份比競爭對手更優秀的詳細文章大綱。
目標關鍵字："{keyword}"

競爭對手分析：
平均字數：{avg_count}
共同主題：{common_topics}

你的任務：
1. 建立一個包含所有共同主題的結構 (H2 -> H3)。
2. 加入競爭對手遺漏的「缺口主題」(Gap Topics)（160% 法則）。
3. 目標總字數：{target_count} 字（必須高於競爭對手平均值）。
4. 返回符合下方 Schema 的有效 JSON。

JSON Schema:
{{
  "title": "文章標題",
  "description": "Meta 描述",
  "target_word_count": 15000,
  "sections": [
    {{
      "id": "1",
      "h2_title": "章節標題",
      "h3_subsections": ["子標題 1", "子標題 2"],
      "key_points": ["重點 1", "重點 2"],
      "target_length": 2000
    }}
  ]
}}
"""

def generate_outline(keyword: str, analysis: CompetitorAnalysis) -> MasterOutline:
    target_count = int(analysis.avg_word_count * 1.6)
    if target_count < 3000: target_count = 3000 # Minimum baseline
    
    prompt = PROMPT_TEMPLATE.format(
        keyword=keyword,
        avg_count=analysis.avg_word_count,
        common_topics=json.dumps(analysis.common_topics[:10], ensure_ascii=False),
        target_count=target_count
    ) + "\n\nIMPORTANT: Return ONLY the raw JSON object. Do not wrap in markdown code blocks. Do not add any conversational text before or after."
    
    response = call_llm(prompt)
    print(f"DEBUG OUTLINE RESPONSE: {response[:100]}...") # Add debug print
    
    if response == "MOCKED_LLM_RESPONSE":
        # Return a dummy outline for testing workflow
        return MasterOutline(
            title=f"{keyword} 完整指南 (Mock)",
            description="Mock description",
            target_word_count=5000,
            sections=[
                SectionState("1", "前言", [], ["Intro"], 500, status="planned"),
                SectionState("2", "重點分析", [], ["Main Point"], 1000, status="planned")
            ]
        )
        
    try:
        data = parse_json_response(response)
        sections = []
        for s in data.get("sections", []):
            sections.append(SectionState(
                id=str(s.get("id", len(sections)+1)),
                h2_title=s.get("h2_title", ""),
                h3_subsections=s.get("h3_subsections", []),
                key_points=s.get("key_points", []),
                target_length=s.get("target_length", 1000),
                status="planned"
            ))
            
        return MasterOutline(
            title=data.get("title", ""),
            description=data.get("description", ""),
            target_word_count=data.get("target_word_count", target_count),
            sections=sections
        )
    except Exception as e:
        print(f"Error parsing outline: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    pass
