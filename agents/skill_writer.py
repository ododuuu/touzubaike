import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# 設定環境
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("找不到 GEMINI_API_KEY，請檢查 .env 檔案")

genai.configure(api_key=api_key)

# 模型設定
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
}

model = genai.GenerativeModel(
    model_name="gemini-2.5-pro", # 使用最新的 2.5 Pro
    generation_config=generation_config,
)

def generate_outline(keyword):
    """
    Skill: SERP Analysis (Simulated)
    分析關鍵字並產生贏過競爭對手的大綱
    """
    print(f"正在分析關鍵字 '{keyword}' 並生成大綱...")
    
    prompt = f"""
    你是一位頂尖的 SEO 內容策略專家。你的目標是針對關鍵字「{keyword}」撰寫一篇能奪得 Google 搜尋排名第一的文章。
    
    請先分析這個關鍵字的搜尋意圖（Search Intent）。使用者想知道什麼？
    假設目前 Google 前三名的文章都包含：定義、運作原理、購買方式、風險。
    
    請為我規劃一份「完勝競爭對手」的文章大綱。
    
    要求：
    1.  標題 (H1)：必須包含關鍵字，且極具吸引力（例如包含年份、教學、懶人包等詞）。
    2.  結構：包含 H2 和 H3。
    3.  內容缺口：找出前三名可能忽略但使用者在乎的痛點（例如：詐騙識別、手續費比較、台灣在地化資訊）。
    4.  字數預估：建議總字數（通常建議 2500 字以上）。
    5.  格式：請直接回傳 JSON 格式，欄位包含 title, description, outline (list of sections)。
    """
    
    response = model.generate_content(prompt)
    # 簡單處理 JSON，Gemini 有時會包在 ```json ... ``` 裡
    text = response.text
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0]
    elif "```" in text:
        text = text.split("```")[1].split("```")[0]
        
    return json.loads(text)

def generate_article(keyword, outline_data):
    """
    Skill: Content Drafting
    根據大綱撰寫完整 Markdown 文章
    """
    print(f"正在撰寫 '{keyword}' 的完整文章...")
    
    outline_str = json.dumps(outline_data, ensure_ascii=False, indent=2)
    
    prompt = f"""
    你是一位專業的財經 SEO 寫手。請根據以下大綱，撰寫一篇完整的 Markdown 文章。
    
    關鍵字：{keyword}
    大綱資料：
    {outline_str}
    
    撰寫規範：
    1.  **Frontmatter**: 務必包含 YAML Frontmatter，欄位：title, description, pubDate (今天), updatedDate (今天), tags (至少 5 個)。
    2.  **語氣**: 專業但親切，適合台灣讀者（使用台灣繁體中文用語，如：存摺、匯款、金管會）。
    3.  **SEO**: 
        - 關鍵字「{keyword}」要在前 200 字自然出現 2-3 次。
        - H2/H3 標題盡量包含長尾關鍵字。
    4.  **格式**:
        - 使用 Markdown。
        - 比較表格請用 Markdown Table。
        - 重點請用 **粗體**。
        - 每個段落不要太長，保持易讀性。
        - 必須包含「常見問題 FAQ」章節。
        - 結尾要有行動呼籲 (CTA)。
    5.  **內容**: 內容必須充實、有深度，不要寫空話。總字數目標 2000 字以上。
    
    請直接輸出 Markdown 內容。
    """
    
    response = model.generate_content(prompt)
    return response.text

def main():
    # 測試用：指定關鍵字
    target_keyword = "usdt是什麼"
    
    try:
        # Step 1: 生成大綱
        outline = generate_outline(target_keyword)
        print("大綱生成成功！")
        # print(json.dumps(outline, ensure_ascii=False, indent=2))
        
        # Step 2: 撰寫文章
        article_content = generate_article(target_keyword, outline)
        
        # 處理 Markdown 輸出 (移除可能的 ```markdown 包裹)
        if article_content.startswith("```markdown"):
            article_content = article_content.replace("```markdown", "", 1)
        if article_content.startswith("```"):
            article_content = article_content.replace("```", "", 1)
        if article_content.endswith("```"):
            article_content = article_content[:-3]
            
        article_content = article_content.strip()

        # Step 3: 存檔
        # 檔名處理：將關鍵字轉為英文 slug (這裡先簡單用硬編碼，之後可用 LLM 轉)
        filename = "usdt-complete-guide-2026.md" 
        output_path = f"src/content/blog/{filename}"
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(article_content)
            
        print(f"文章已生成並儲存於: {output_path}")
        
    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    main()
