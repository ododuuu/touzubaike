# SEO Skill - Programmatic SEO Content Generation

智能 SEO 內容生成系統，用於批量生成詐騙防範、交易所教學等 SEO 優化頁面。

## 使用方式

```bash
# 生成單一詐騙防範頁面
/seo generate bitopro
/seo generate usdt
/seo generate okx

# 列出所有可用平台
/seo list

# 批量生成所有頁面
/seo batch

# 分析 SEO 表現
/seo analyze bitopro
```

## 功能

### 1. 內容生成 (generate)
- 基於模板和數據自動生成 Markdown 內容
- 使用 LLM 豐富化內容（FAQ、案例、結論）
- SEO 優化檢查（標題、描述、關鍵詞密度）
- 自動生成 frontmatter

### 2. 平台列表 (list)
- 顯示所有可用的詐騙平台 ID
- 顯示平台類型、合法性、台灣牌照狀態

### 3. 批量生成 (batch)
- 一次生成所有平台的詐騙防範頁面
- 自動控制 API 呼叫頻率避免 rate limit

### 4. SEO 分析 (analyze)
- 檢查現有頁面的 SEO 分數
- 提供改進建議

## 系統架構

```
tools/seo_agent/          # Python 後端
├── data/                 # 平台數據
├── templates/            # 頁面模板
├── skills/               # Python 模組
└── main.py               # CLI 入口

.claude/skills/           # Claude Code 前端
└── seo.md                # Skill 定義（本檔案）
```

## 環境變數

```bash
export GEMINI_API_KEY='your-api-key-here'
```

## 參數說明

- `platform`: 平台 ID（如 bitopro, usdt, okx）
- `--dry-run`: 預覽模式，不實際儲存檔案

## 範例

```bash
# 對話式使用
User: /seo generate bitopro
Assistant: 正在生成 BitoPro 詐騙防範頁面...
✓ 模板渲染完成
✓ LLM 內容豐富化完成
✓ SEO 檢查通過 (83/100)
✓ 檔案已儲存: src/content/blog/scam/bitopro.md

# 批量使用
User: /seo batch
Assistant: 批量生成 9 個詐騙防範頁面...
[1/9] bitopro ✓
[2/9] usdt ✓
...
完成！成功: 9, 失敗: 0
```

## 技術細節

**工作流程**:
1. 載入平台數據 (scam_data_loader.py)
2. 渲染模板 (scam_template_renderer.py)
3. LLM 豐富化 (scam_content_enricher.py)
4. SEO 優化檢查 (seo_optimizer.py)
5. 儲存 Markdown 檔案

**SEO 標準**:
- 標題: 20-60 字元
- 描述: 80-160 字元
- 內容: ≥1500 字
- H2 標題: ≥3 個
- 關鍵詞密度: 3-5 次

## 擴展性

未來可擴展的模板類型:
- 交易所操作指南 (exchange_operation)
- 交易所評測 (exchange_review)
- 幣種介紹 (coin_intro)
- 投資策略 (strategy_guide)
