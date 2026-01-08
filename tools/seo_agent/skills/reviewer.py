
import sys
import os
from typing import List, Tuple

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from skills.llm_client import call_llm

PROMPT_TEMPLATE = """
你是一位專家級的 SEO 編輯。
任務：審查以下的部落格章節草稿。
檢查清單：
1. 目標關鍵字 "{keyword}" 是否自然地出現？
2. 語氣是否像真人（Dcard/PTT 風格）且專業？
3. 是否至少有 2 個清晰的段落？
4. 如果該章節是在比較事物，是否有包含表格？

草稿內容：
{draft}

輸出格式：JSON
{{
  "score": 85,
  "feedback": ["語氣不錯。", "缺少關於 X 的具體數據。"]
}}
"""

def review_draft(draft: str, keyword: str) -> Tuple[int, List[str]]:
    prompt = PROMPT_TEMPLATE.format(keyword=keyword, draft=draft[:2000]) # Truncate for safety
    response = call_llm(prompt)
    
    if response == "MOCKED_LLM_RESPONSE":
        return 90, ["Mocked feedback: Looks good."]
        
    try:
        # Naive parsing
        import json
        clean = response.strip().strip("`").replace("json", "")
        data = json.loads(clean)
        return data.get("score", 0), data.get("feedback", [])
    except:
        return 70, ["Error parsing review response."]

if __name__ == "__main__":
    pass
