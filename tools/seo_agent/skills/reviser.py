
import sys
import os
from typing import List

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from skills.llm_client import call_llm

PROMPT_TEMPLATE = """
你是一位專家級的內容修訂者。
任務：根據編輯的回饋重新撰寫以下草稿。

回饋：
{feedback}

原始草稿：
{draft}

請只返回修訂後的 Markdown 內容。
"""

def revise_draft(draft: str, feedback: List[str]) -> str:
    prompt = PROMPT_TEMPLATE.format(
        feedback="\n".join(feedback),
        draft=draft
    )
    
    response = call_llm(prompt)
    
    if response == "MOCKED_LLM_RESPONSE":
        return draft + "\n\n(已根據回饋修訂)"
        
    return response

if __name__ == "__main__":
    pass
