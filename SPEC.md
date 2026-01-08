# 投資百科 - 網站規格書與操作手冊

## 一、網站架構

### 技術棧
- **框架**: Astro 5.x
- **樣式**: Tailwind CSS 4.x
- **內容**: Markdown + Content Collections
- **部署**: GitHub + Cloudflare Pages（免費）

### 目錄結構
```
/seo-site
├── src/
│   ├── content/blog/     # ← 文章放這裡（Markdown）
│   ├── components/       # 網站元件
│   ├── layouts/          # 頁面模板
│   ├── pages/            # 路由頁面
│   └── styles/           # 全域樣式
├── public/images/        # ← 圖片放這裡
├── astro.config.mjs      # ← 網站設定（網域）
└── package.json
```

---

## 二、文章撰寫規範

### 文章 Frontmatter 模板
```markdown
---
title: "[年份] 最新｜[關鍵字]？[副標題]"
description: "[關鍵字]...[關鍵字]...[吸引點擊的描述，2-3 次關鍵字]"
pubDate: "2026-01-08"
updatedDate: "2026-01-08"
tags: ["標籤1", "標籤2", "標籤3"]
---
```

### SEO 寫作檢查清單

#### Title 標題
- [ ] 關鍵字放在標題最前面
- [ ] 關鍵字出現 1-2 次
- [ ] 標題長度 25-35 字

#### Meta Description
- [ ] 關鍵字出現 2-3 次
- [ ] 長度 80-150 字
- [ ] 有吸引點擊的元素

#### 內容
- [ ] 前 200 字放 2-3 次關鍵字
- [ ] 總字數 2000-4000 字
- [ ] 滿足搜尋意圖
- [ ] H2/H3 標題含關鍵字（不勉強）

#### 連結
- [ ] 內部連結 3-4 個
- [ ] 外部權威連結 1-2 個（Wikipedia、政府網站、官方網站）

#### 其他
- [ ] 有比較表格
- [ ] 有 FAQ 區塊
- [ ] 結尾有行動呼籲（CTA）
- [ ] 圖片有 alt 文字

---

## 三、寫一篇新文章的步驟

### Step 1: 建立檔案
在 `src/content/blog/` 新增 `.md` 檔案，例如：
```
src/content/blog/max-exchange-guide.md
```

### Step 2: 填入 Frontmatter
```markdown
---
title: "MAX 交易所完整教學｜開戶、入金、買幣一次搞懂"
description: "MAX 交易所怎麼用？這篇教你 MAX 交易所開戶、台幣入金、購買 USDT 的完整流程，新手 10 分鐘上手。"
pubDate: "2026-01-08"
tags: ["MAX", "交易所", "入金教學"]
---
```

### Step 3: 撰寫內容
按照 H2 → H3 結構撰寫，記得：
- 開頭點破重點
- 每個 H2 都是一個獨立章節
- 結尾放 CTA

### Step 4: 本地預覽
```bash
npm run dev
```
瀏覽 http://localhost:4321/blog/[檔名]/ 確認顯示正確

---

## 四、部署到 Cloudflare Pages

### 前置準備
1. 註冊 [GitHub](https://github.com/) 帳號
2. 註冊 [Cloudflare](https://dash.cloudflare.com/) 帳號

### Step 1: 推送到 GitHub
```bash
# 在 seo-site 目錄執行
git remote add origin https://github.com/你的帳號/你的repo名稱.git
git branch -M main
git push -u origin main
```

### Step 2: 連接 Cloudflare Pages
1. 登入 [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. 左側選單點「Workers & Pages」
3. 點「Create」→「Pages」→「Connect to Git」
4. 授權 GitHub，選擇你的 repo
5. 設定如下：
   - **Framework preset**: Astro
   - **Build command**: `npm run build`
   - **Build output directory**: `dist`
6. 點「Save and Deploy」

### Step 3: 設定自訂網域（可選）
1. 在 Cloudflare Pages 專案裡點「Custom domains」
2. 輸入你的網域（例如 `touzubaike.com`）
3. 按照指示設定 DNS

### Step 4: 提交 Sitemap 到 Google Search Console
1. 前往 [Google Search Console](https://search.google.com/search-console)
2. 新增網站資源
3. 左側選「Sitemap」
4. 輸入 `sitemap-index.xml` 並提交

---

## 五、文章待辦清單

### 已完成
- [x] USDT 是什麼？

### 待撰寫（優先度高）
- [ ] MAX 交易所完整教學
- [ ] BitoPro 交易所完整教學
- [ ] 加密貨幣入金指南（台幣怎麼變成 USDT）
- [ ] 穩定幣是什麼？USDT vs USDC 比較

### 待撰寫（中)
- [ ] 幣安註冊教學
- [ ] 什麼是區塊鏈？
- [ ] 比特幣是什麼？
- [ ] 以太幣是什麼？

---

## 六、網站設定修改

### 修改網站名稱/描述
編輯 `src/consts.ts`：
```typescript
export const SITE_TITLE = '投資百科';
export const SITE_DESCRIPTION = '加密貨幣、股票、ETF、信用卡——投資理財一站式指南。';
```

### 修改網域（上線前必做）
編輯 `astro.config.mjs`：
```javascript
export default defineConfig({
  site: 'https://你的網域.com',  // ← 改這裡
  ...
});
```

---

## 七、日常維護

### 更新文章
1. 修改 Markdown 檔案
2. 更新 `updatedDate` 欄位
3. `git add . && git commit -m "更新文章" && git push`
4. Cloudflare 會自動重新部署

### 新增文章
1. 在 `src/content/blog/` 新增 `.md` 檔案
2. 本地預覽確認
3. `git add . && git commit -m "新增文章" && git push`

### 查看流量
1. Google Search Console → 成效報告
2. Google Analytics（需另外設定）
