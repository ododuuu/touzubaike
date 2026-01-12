import pandas as pd
import json
import os
import glob
from dotenv import load_dotenv

# 設定環境
load_dotenv()

# 設定參數
RANK_THRESHOLD_MIN = 1
RANK_THRESHOLD_MAX = 20
IMPRESSION_THRESHOLD = 500  # 曝光門檻，可根據需求調整

def find_gsc_file(downloads_path):
    # 尋找最新的 murmurcats GSC 資料夾
    pattern = os.path.join(downloads_path, "murmurcats.com-Performance-on-Search-*")
    folders = glob.glob(pattern)
    if not folders:
        print("Error: 找不到 murmurcats GSC 資料夾")
        return None
    
    # 找最新的資料夾
    latest_folder = max(folders, key=os.path.getmtime)
    csv_path = os.path.join(latest_folder, "查詢.csv")
    
    if not os.path.exists(csv_path):
        print(f"Error: 找不到 {csv_path}")
        return None
        
    return csv_path

def analyze_keywords():
    downloads_path = "/Users/wang/Downloads"
    csv_file = find_gsc_file(downloads_path)
    
    if not csv_file:
        return

    print(f"正在分析: {csv_file}")
    
    try:
        df = pd.read_csv(csv_file)
        
        # 轉換數據類型
        # 點閱率原始格式可能為 "16.7%" 需要轉為 float
        if df['點閱率'].dtype == object:
            df['點閱率'] = df['點閱率'].str.rstrip('%').astype('float') / 100
            
        # 篩選條件
        # 1. 排名在 1~20 之間
        rank_mask = (df['排名'] >= RANK_THRESHOLD_MIN) & (df['排名'] <= RANK_THRESHOLD_MAX)
        # 2. 曝光量足夠
        impression_mask = df['曝光'] >= IMPRESSION_THRESHOLD
        
        target_keywords = df[rank_mask & impression_mask].copy()
        
        # 計算「進攻分數」(Opportunity Score)
        # 邏輯：高曝光 + 低點擊 = 潛力大 (可以搶過來)
        # 簡單公式：曝光 * (1 - CTR) (未被滿足的需求量)
        target_keywords['opportunity_score'] = target_keywords['曝光'] * (1 - target_keywords['點閱率'])
        
        # 排序
        result = target_keywords.sort_values(by='opportunity_score', ascending=False).head(20)
        
        # 輸出 JSON
        output_data = []
        for _, row in result.iterrows():
            output_data.append({
                "keyword": row['熱門查詢項目'],
                "rank": row['排名'],
                "impressions": int(row['曝光']),
                "ctr": float(row['點閱率']),
                "score": int(row['opportunity_score'])
            })
            
        output_file = "target_keywords.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
            
        print(f"分析完成！已找出 {len(output_data)} 個潛力關鍵字，儲存於 {output_file}")
        
        # 顯示前 5 名
        print("\nTop 5 潛力關鍵字:")
        for item in output_data[:5]:
            print(f"- {item['keyword']} (排名: {item['rank']}, 曝光: {item['impressions']}, CTR: {item['ctr']:.1%})")

    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    analyze_keywords()
