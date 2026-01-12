import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

generation_config = {
    "temperature": 0.5,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
}

model = genai.GenerativeModel(
    model_name="gemini-2.5-pro",
    generation_config=generation_config,
)

def complete_article(file_path):
    """
    Skill: Auto-Completion
    檢查文章是否完整，若未完成則補完結尾
    """
    print(f"正在檢查文章完整性: {file_path}")
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # 簡單判斷：檢查最後是否為句號或常見結尾符號
        # 如果最後一行看起來像是斷句，則觸發補完
        last_chars = content.strip()[-10:]
        print(f"文章結尾預覽: ...{last_chars}")
        
        # 這裡的邏輯可以更複雜，例如檢查是否有 "CTA" 區塊
        # 簡單起見，我們假設如果最後一個字元不是標點符號，就是斷了
        if last_chars[-1] not in ["。", "！", "？", "}", ">", ")"]:
            print("偵測到文章未完成，開始補完...")
            
            # 取文章最後 2000 個字作為 context
            context = content[-2000:]
            
            prompt = f"""
            以下是一篇未寫完的 Markdown 文章的結尾部分。請你接著寫完它。
            
            要求：
            1.  接續語氣，完成最後一個段落。
            2.  補上一個強而有力的結尾總結 (Conclusion)。
            3.  補上行動呼籲 (CTA)，鼓勵讀者分享或訂閱。
            4.  只輸出補完的內容，不要重複前面的內容。
            
            文章結尾 context:
            {context}
            """
            
            response = model.generate_content(prompt)
            completion = response.text
            
            # 清理輸出
            if completion.startswith("```markdown"):
                completion = completion.replace("```markdown", "", 1)
            if completion.startswith("```"):
                completion = completion.replace("```", "", 1)
            if completion.endswith("```"):
                completion = completion[:-3]
                
            # 將補完內容附加到檔案
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(completion)
                
            print("文章已補完！")
        else:
            print("文章看起來是完整的，無需補完。")
            
    except Exception as e:
        print(f"補完過程發生錯誤: {e}")

if __name__ == "__main__":
    # 測試用
    target_file = "src/content/blog/usdt-complete-guide-2026.md"
    complete_article(target_file)
