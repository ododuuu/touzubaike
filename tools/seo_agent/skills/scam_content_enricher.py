"""
Scam Content Enricher - LLM 內容豐富化模組
調用 LLM 生成 FAQ、案例、結論等動態內容
"""

import json
from typing import Dict, List
from .llm_client import call_llm, parse_json_response
from .scam_data_loader import ScamPlatform


class ScamContentEnricher:
    """使用 LLM 豐富化詐騙防範頁面內容"""

    def __init__(self, model: str = "gemini-2.0-flash"):
        self.model = model

    def enrich(self, rendered_content: Dict) -> str:
        """
        豐富化模板內容，填充所有佔位符

        Args:
            rendered_content: ScamTemplateRenderer.render() 的輸出

        Returns:
            完整的 Markdown 內容
        """
        markdown = rendered_content['markdown']
        platform = rendered_content['platform']
        metadata = rendered_content['metadata']

        # 生成各區塊內容
        intro = self._generate_intro(platform, metadata)
        faq = self._generate_faq(platform)
        conclusion = self._generate_conclusion(platform)

        # 填充佔位符
        markdown = markdown.replace("{intro_section}", intro)
        markdown = markdown.replace("{faq_section}", faq)
        markdown = markdown.replace("{conclusion_section}", conclusion)

        return markdown

    def _generate_intro(self, platform: ScamPlatform, metadata: Dict) -> str:
        """生成開場白"""
        prompt = f"""你是一位台灣的加密貨幣安全專家，正在撰寫一篇關於「{platform.chinese_name}詐騙」的防範指南。

平台資訊：
- 名稱：{platform.name}（{platform.chinese_name}）
- 類型：{platform.platform_type}
- 是否合法：{platform.is_legit}
- 主要關鍵詞：{', '.join(platform.keywords[:3])}

請用繁體中文撰寫一段 150-200 字的開場白，要求：
1. 用親切但專業的語氣
2. 直接切入主題，說明為什麼要寫這篇文章
3. 簡述台灣近期的詐騙趨勢
4. 讓讀者知道讀完這篇能學到什麼
5. 不要用「大家好」這種開頭

直接輸出開場白文字，不要加任何標記或說明。"""

        response = call_llm(prompt, self.model)

        if response == "MOCKED_LLM_RESPONSE":
            return self._fallback_intro(platform)

        return response.strip()

    def _generate_faq(self, platform: ScamPlatform) -> str:
        """生成 FAQ 區塊"""
        prompt = f"""你是一位台灣的加密貨幣安全專家，請針對「{platform.chinese_name}詐騙」生成 5-6 個常見問題。

平台資訊：
- 名稱：{platform.name}（{platform.chinese_name}）
- 類型：{platform.platform_type}
- 是否合法：{platform.is_legit}
- 常見詐騙手法：{', '.join([st.name for st in platform.common_scam_types[:3]])}

請用以下 JSON 格式回傳：
```json
{{
  "faqs": [
    {{"question": "問題1", "answer": "回答1（50-100字）"}},
    {{"question": "問題2", "answer": "回答2（50-100字）"}}
  ]
}}
```

要求：
1. 使用繁體中文
2. 問題要符合台灣用戶的搜尋習慣
3. 回答要實用、簡潔
4. 包含至少一個「被騙了怎麼辦」的問題
5. 包含至少一個「如何辨識」的問題"""

        response = call_llm(prompt, self.model)

        if response == "MOCKED_LLM_RESPONSE":
            return self._fallback_faq(platform)

        try:
            data = parse_json_response(response)
            return self._format_faq(data.get("faqs", []))
        except (json.JSONDecodeError, KeyError):
            return self._fallback_faq(platform)

    def _generate_conclusion(self, platform: ScamPlatform) -> str:
        """生成結論"""
        prompt = f"""你是一位台灣的加密貨幣安全專家，正在撰寫「{platform.chinese_name}詐騙防範指南」的結論。

平台資訊：
- 名稱：{platform.name}（{platform.chinese_name}）
- 是否合法：{platform.is_legit}

請用繁體中文撰寫 100-150 字的結論，要求：
1. 總結本文重點
2. 強調謹慎投資的重要性
3. 提醒讀者遇到可疑情況要立即求證
4. 用正面但謹慎的語氣結尾
5. 不要重複前面已經說過的內容

直接輸出結論文字，不要加任何標記或說明。"""

        response = call_llm(prompt, self.model)

        if response == "MOCKED_LLM_RESPONSE":
            return self._fallback_conclusion(platform)

        return response.strip()

    def _format_faq(self, faqs: List[Dict]) -> str:
        """格式化 FAQ 為 Markdown"""
        lines = []
        for faq in faqs:
            q = faq.get("question", "")
            a = faq.get("answer", "")
            lines.append(f"### {q}")
            lines.append("")
            lines.append(a)
            lines.append("")
        return "\n".join(lines)

    # === Fallback 內容（當 LLM 不可用時）===

    def _fallback_intro(self, platform: ScamPlatform) -> str:
        """備用開場白"""
        if platform.platform_type == "scam_pattern":
            return f"""近年來，「{platform.chinese_name}」在台灣造成大量金錢損失，根據165反詐騙專線統計，相關案件逐年攀升。本文將深入剖析{platform.chinese_name}的運作模式、常見手法，並提供實用的辨識技巧和自救方法，幫助你保護自己和家人遠離詐騙陷阱。"""
        else:
            return f"""「{platform.chinese_name}是詐騙嗎？」這是許多台灣投資人心中的疑問。事實上，{platform.name}本身是{'合法的' if platform.is_legit else '有爭議的'}交易平台，但詐騙集團經常假冒其名義行騙。本文將完整解析常見的{platform.chinese_name}詐騙手法，教你如何辨識真假，以及萬一受騙後的自救流程。"""

    def _fallback_faq(self, platform: ScamPlatform) -> str:
        """備用 FAQ"""
        faqs = [
            {
                "question": f"{platform.chinese_name}是詐騙嗎？",
                "answer": f"{platform.name}本身{'是合法的平台' if platform.is_legit else '存在風險'}，但詐騙集團經常假冒其名義進行詐騙，使用前請務必確認是否為官方管道。"
            },
            {
                "question": f"遇到{platform.chinese_name}詐騙怎麼辦？",
                "answer": "請立即停止匯款，保留所有對話記錄和轉帳憑證，撥打165反詐騙專線諮詢，並盡快到警局報案。"
            },
            {
                "question": f"如何辨識假的{platform.chinese_name}？",
                "answer": f"確認網址是否為官方域名、不要點擊來路不明的連結、官方不會主動要求你提供密碼或私鑰。"
            },
            {
                "question": "被騙的錢拿得回來嗎？",
                "answer": "追回機率較低，但仍建議報案。若是透過台灣銀行轉帳，可嘗試聯繫銀行止付。若是加密貨幣轉帳，追回難度極高。"
            },
            {
                "question": "如何舉報詐騙網站？",
                "answer": "可向165反詐騙專線、警政署刑事局網路犯罪報案系統、金管會陳情，協助阻斷詐騙集團。"
            }
        ]
        return self._format_faq(faqs)

    def _fallback_conclusion(self, platform: ScamPlatform) -> str:
        """備用結論"""
        return f"""投資加密貨幣前，請務必做好功課，確認平台的合法性和安全性。遇到保證獲利、高額報酬等說詞時，請提高警覺。若發現可疑情況，立即透過官方管道查證，並向165反詐騙專線諮詢。保護好自己的資產，遠離詐騙陷阱。"""


def enrich_scam_content(rendered_content: Dict) -> str:
    """便捷函式：豐富化詐騙防範內容"""
    enricher = ScamContentEnricher()
    return enricher.enrich(rendered_content)


if __name__ == "__main__":
    # 測試
    from .scam_template_renderer import ScamTemplateRenderer

    renderer = ScamTemplateRenderer()
    enricher = ScamContentEnricher()

    print("=== 測試 BitoPro 內容豐富化 ===")
    rendered = renderer.render("bitopro")
    enriched = enricher.enrich(rendered)

    print("\n=== 豐富化後的 Markdown（前 3000 字）===")
    print(enriched[:3000])
