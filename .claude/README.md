# Claude Code Skills for TouZuBaike

專為 TouZuBaike SEO 網站打造的 Claude Code Skills。

## 可用 Skills

### `/seo` - SEO 內容生成器

Programmatic SEO 內容生成系統，支援批量生成詐騙防範、交易所教學等 SEO 優化頁面。

## 快速開始

### 1. 對話式使用（推薦）

在 Claude Code 對話中直接使用：

```bash
# 生成單一頁面
/seo generate bitopro

# 查看所有可用平台
/seo list

# 批量生成所有頁面
/seo batch

# 分析現有頁面的 SEO
/seo analyze bitopro

# 部署到 Git
/seo deploy
```

### 2. 終端批量使用

適合 CI/CD 或定期更新：

```bash
cd tools/seo_agent

# 列出平台
python3 main.py scam-list

# 生成單一頁面
export GEMINI_API_KEY='your-api-key'
python3 main.py scam-generate --platform bitopro

# 批量生成
python3 main.py scam-generate-all

# 部署
python3 main.py scam-deploy
```

## 系統架構

```
touzubaike/
├── .claude/                      # Claude Code Skills
│   ├── skills/
│   │   ├── seo.md               # Skill 說明文件
│   │   └── seo-wrapper.sh       # Skill 執行腳本
│   ├── skills.json              # Skill 註冊
│   └── README.md                # 本檔案
│
├── tools/seo_agent/             # Python 後端系統
│   ├── data/
│   │   └── scam_platforms.json  # 平台數據
│   ├── templates/
│   │   └── scam_guide.md        # 頁面模板
│   ├── skills/
│   │   ├── scam_data_loader.py
│   │   ├── scam_template_renderer.py
│   │   ├── scam_content_enricher.py
│   │   └── seo_optimizer.py
│   └── main.py                  # CLI 入口
│
└── src/content/blog/scam/       # 生成的內容
    ├── bitopro.md
    ├── usdt.md
    └── ...
```

## 工作流程

### 對話式工作流

1. **生成內容**
   ```bash
   User: /seo generate bitopro
   Claude: 正在生成 BitoPro 詐騙防範頁面...
           ✓ 模板渲染完成
           ✓ LLM 內容豐富化完成
           ✓ SEO 檢查通過 (83/100)
           ✓ 檔案已儲存
   ```

2. **檢查品質**
   ```bash
   User: /seo analyze bitopro
   Claude: SEO Score: 83/100
           Word Count: 2226
           Issues: [列出改進建議]
   ```

3. **批量生成**
   ```bash
   User: /seo batch
   Claude: 批量生成 9 個頁面...
           [進度顯示]
           完成！成功: 9, 失敗: 0
   ```

4. **部署**
   ```bash
   User: /seo deploy
   Claude: ✓ Git commit
           ✓ Git push
           已部署到 GitHub
   ```

### 批量自動化工作流

適合定期更新或 CI/CD：

```bash
# 每週自動更新
cd tools/seo_agent
export GEMINI_API_KEY='...'

# 重新生成所有頁面（使用最新數據和模板）
python3 main.py scam-generate-all

# 自動部署
git add src/content/blog/scam/
git commit -m "Weekly content update"
git push
```

## 環境設定

### 必要環境變數

```bash
export GEMINI_API_KEY='your-api-key-here'
```

### 可選設定

在 `tools/seo_agent/main.py` 中調整：
- LLM 模型（預設: gemini-2.0-flash）
- SEO 標準（標題長度、字數等）
- 批量生成延遲（避免 API rate limit）

## SEO 標準

系統會自動檢查以下 SEO 指標：

| 項目 | 標準 |
|------|------|
| 標題長度 | 20-60 字元 |
| 描述長度 | 80-160 字元 |
| 內容字數 | ≥1500 字 |
| H2 標題數 | ≥3 個 |
| 關鍵詞密度 | 3-5 次 |
| 內部連結 | 2-5 個 |

## 擴展功能

### 新增平台

編輯 `tools/seo_agent/data/scam_platforms.json`：

```json
{
  "id": "new-platform",
  "name": "Platform Name",
  "chinese_name": "中文名稱",
  "type": "taiwan_exchange",
  "keywords": ["關鍵詞1", "關鍵詞2"],
  "common_scam_types": [
    {"name": "詐騙類型", "description": "說明"}
  ],
  "is_legit": true,
  "taiwan_licensed": false
}
```

### 新增模板類型

未來可擴展：
- 交易所操作指南 (exchange_operation)
- 交易所評測 (exchange_review)
- 幣種介紹 (coin_intro)
- 投資策略 (strategy_guide)

## 故障排除

### Skill 無法使用

檢查：
1. `.claude/skills/seo-wrapper.sh` 是否有執行權限
2. `GEMINI_API_KEY` 是否設定
3. Python 依賴是否安裝

### SEO 分數過低

常見問題：
- 描述太短 → 修改 `scam_template_renderer.py`
- 關鍵詞密度不足 → 調整模板
- 內部連結不足 → 手動加入相關文章連結

### LLM 生成失敗

檢查：
- API Key 是否有效
- 網路連線是否正常
- API quota 是否用完

系統會自動使用 fallback 內容，確保即使 LLM 失敗也能生成基礎頁面。

## 維護

### 定期任務

- **每週**：重新生成內容，更新數據
- **每月**：檢查 SEO 表現，調整關鍵詞
- **季度**：擴展新平台、新模板類型

### 監控指標

- SEO 分數平均值
- 生成成功率
- LLM API 使用量
- 頁面流量（透過 GSC）
