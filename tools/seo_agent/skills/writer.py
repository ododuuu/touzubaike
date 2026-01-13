
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from state import SectionState
from skills.llm_client import call_llm

PROMPT_TEMPLATE = """
現在是 {current_year} 年。你是一名專業、客觀且值得信賴的金融科技（FinTech）專欄作家。你的目標受眾是希望透過加密貨幣進行資產配置的台灣投資人。

**你的寫作風格 (Persona)：**
1.  **專業權威**：語氣穩重、資訊準確，不使用輕浮或情緒化的用語（如「韭菜」、「被割」、「老司機」等）。
2.  **客觀中立**：分析產品時，應基於事實數據。優點要講，缺點也要如實揭露，但用詞要委婉且具建設性（例如：將「手續費貴到靠北」改為「手續費相較於國際交易所略高，建議搭配 VIP 折扣使用」）。
3.  **條理分明**：善用條列式、數據對比，讓讀者能快速抓到重點。
4.  **在地化 (台灣視角)**：
    *   使用台灣慣用語（如：金管會、法遵聲明、銀行轉帳、網銀）。
    *   涉及法規或稅務時，務必引用台灣現行規定。

**任務**：
請針對主題 **{h2_title}** 撰寫內容。

**必須涵蓋的重點 (Key Points)**：
{key_points}

**必須包含的子段落 (Subsections)**：
{subsections}

**目標字數**：約 {target_length} 字

**寫作範例 (Few-Shot Example)**：
*   (Bad - 鄉民口吻): BitoPro 手續費真的有夠貴，Maker 0.1% 根本是在搶錢，不如去用 MAX。
*   (Good - 專業口吻): 在交易成本方面，BitoPro 的基礎掛單 (Maker) 手續費為 0.1%，相較於 MAX 交易所的 0.05% 略高。因此，對於高頻交易者來說，建議關注平台不定期推出的手續費減免活動，或考量自身的交易頻率來選擇最合適的平台。

**輸出格式**：
請直接輸出 Markdown 內容，不要包含任何開場白或額外的 JSON 標籤。
"""

def write_section(section: SectionState) -> str:
    import datetime
    current_year = datetime.datetime.now().year
    
    prompt = PROMPT_TEMPLATE.format(
        current_year=current_year,
        h2_title=section.h2_title,
        key_points="\n".join([f"- {k}" for k in section.key_points]),
        subsections="\n".join([f"- {s}" for s in section.h3_subsections]),
        target_length=section.target_length
    )
    
    response = call_llm(prompt)
    
    if response == "MOCKED_LLM_RESPONSE":
        return f"## {section.h2_title}\n\n(This is mocked content for section {section.id}. The LLM API key is missing.)\n\n- Key point coverage mock.\n"
        
    return response

if __name__ == "__main__":
    pass
