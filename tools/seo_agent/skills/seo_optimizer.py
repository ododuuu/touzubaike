"""
SEO Optimizer - SEO 優化檢查與修正模組
檢查標題長度、meta description、內部連結等
"""

import re
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class SEOIssue:
    severity: str  # "error", "warning", "info"
    category: str
    message: str
    suggestion: str


class SEOOptimizer:
    """SEO 優化檢查器"""

    # SEO 規則設定
    TITLE_MIN_LENGTH = 20
    TITLE_MAX_LENGTH = 60
    TITLE_RECOMMENDED_MAX = 55

    DESC_MIN_LENGTH = 80
    DESC_MAX_LENGTH = 160
    DESC_RECOMMENDED_MAX = 155

    MIN_HEADINGS = 3
    MIN_WORD_COUNT = 1500

    def __init__(self):
        self.issues: List[SEOIssue] = []

    def analyze(self, markdown: str, metadata: Dict) -> Dict:
        """
        分析 Markdown 內容的 SEO 問題

        Returns:
            Dict with:
            - 'score': SEO 分數 (0-100)
            - 'issues': 問題列表
            - 'stats': 統計資訊
        """
        self.issues = []

        # 檢查各項 SEO 元素
        self._check_title(metadata.get('title', ''))
        self._check_description(metadata.get('description', ''))
        self._check_headings(markdown)
        self._check_content_length(markdown)
        self._check_keyword_usage(markdown, metadata.get('keywords', []))
        self._check_internal_links(markdown)
        self._check_images(markdown)

        # 計算分數
        score = self._calculate_score()

        # 統計資訊
        stats = self._get_stats(markdown, metadata)

        return {
            'score': score,
            'issues': self.issues,
            'stats': stats,
            'passed': score >= 70
        }

    def optimize(self, markdown: str, metadata: Dict) -> Tuple[str, Dict]:
        """
        自動優化 Markdown 內容

        Returns:
            Tuple of (optimized_markdown, updated_metadata)
        """
        optimized = markdown
        updated_metadata = metadata.copy()

        # 優化標題長度
        if len(metadata.get('title', '')) > self.TITLE_MAX_LENGTH:
            updated_metadata['title'] = self._truncate_title(metadata['title'])

        # 優化描述長度
        if len(metadata.get('description', '')) > self.DESC_MAX_LENGTH:
            updated_metadata['description'] = self._truncate_description(metadata['description'])

        # 添加內部連結建議
        optimized = self._add_internal_links(optimized, metadata)

        return optimized, updated_metadata

    def _check_title(self, title: str):
        """檢查標題"""
        length = len(title)

        if length < self.TITLE_MIN_LENGTH:
            self.issues.append(SEOIssue(
                severity="error",
                category="title",
                message=f"標題太短（{length} 字）",
                suggestion=f"標題建議至少 {self.TITLE_MIN_LENGTH} 字以上"
            ))
        elif length > self.TITLE_MAX_LENGTH:
            self.issues.append(SEOIssue(
                severity="error",
                category="title",
                message=f"標題太長（{length} 字），會被截斷",
                suggestion=f"標題建議不超過 {self.TITLE_RECOMMENDED_MAX} 字"
            ))
        elif length > self.TITLE_RECOMMENDED_MAX:
            self.issues.append(SEOIssue(
                severity="warning",
                category="title",
                message=f"標題略長（{length} 字）",
                suggestion=f"標題建議不超過 {self.TITLE_RECOMMENDED_MAX} 字"
            ))

    def _check_description(self, description: str):
        """檢查 meta description"""
        length = len(description)

        if length < self.DESC_MIN_LENGTH:
            self.issues.append(SEOIssue(
                severity="error",
                category="description",
                message=f"描述太短（{length} 字）",
                suggestion=f"描述建議至少 {self.DESC_MIN_LENGTH} 字"
            ))
        elif length > self.DESC_MAX_LENGTH:
            self.issues.append(SEOIssue(
                severity="error",
                category="description",
                message=f"描述太長（{length} 字），會被截斷",
                suggestion=f"描述建議不超過 {self.DESC_RECOMMENDED_MAX} 字"
            ))

    def _check_headings(self, markdown: str):
        """檢查標題結構"""
        h2_pattern = r'^## .+$'
        h3_pattern = r'^### .+$'

        h2_count = len(re.findall(h2_pattern, markdown, re.MULTILINE))
        h3_count = len(re.findall(h3_pattern, markdown, re.MULTILINE))

        if h2_count < self.MIN_HEADINGS:
            self.issues.append(SEOIssue(
                severity="warning",
                category="structure",
                message=f"H2 標題數量不足（{h2_count} 個）",
                suggestion=f"建議至少 {self.MIN_HEADINGS} 個 H2 標題"
            ))

        # 檢查是否有 H1
        h1_pattern = r'^# .+$'
        h1_count = len(re.findall(h1_pattern, markdown, re.MULTILINE))
        if h1_count == 0:
            self.issues.append(SEOIssue(
                severity="error",
                category="structure",
                message="缺少 H1 標題",
                suggestion="每頁應有一個 H1 標題"
            ))
        elif h1_count > 1:
            self.issues.append(SEOIssue(
                severity="warning",
                category="structure",
                message=f"H1 標題過多（{h1_count} 個）",
                suggestion="每頁建議只有一個 H1 標題"
            ))

    def _check_content_length(self, markdown: str):
        """檢查內容長度"""
        # 移除 Markdown 語法，計算純文字長度
        text = re.sub(r'```[\s\S]*?```', '', markdown)  # 移除程式碼區塊
        text = re.sub(r'[#*`\[\]()>-]', '', text)  # 移除 Markdown 符號
        text = re.sub(r'\s+', '', text)  # 移除空白

        word_count = len(text)

        if word_count < self.MIN_WORD_COUNT:
            self.issues.append(SEOIssue(
                severity="warning",
                category="content",
                message=f"內容長度偏短（約 {word_count} 字）",
                suggestion=f"建議至少 {self.MIN_WORD_COUNT} 字以上"
            ))

    def _check_keyword_usage(self, markdown: str, keywords: List[str]):
        """檢查關鍵詞使用"""
        if not keywords:
            return

        primary_keyword = keywords[0] if keywords else ""
        if primary_keyword:
            count = markdown.lower().count(primary_keyword.lower())
            if count < 3:
                self.issues.append(SEOIssue(
                    severity="warning",
                    category="keyword",
                    message=f"主關鍵詞「{primary_keyword}」出現次數偏少（{count} 次）",
                    suggestion="建議主關鍵詞至少出現 3-5 次"
                ))

    def _check_internal_links(self, markdown: str):
        """檢查內部連結"""
        # 檢查是否有任何連結
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        links = re.findall(link_pattern, markdown)

        internal_links = [l for l in links if not l[1].startswith('http')]
        external_links = [l for l in links if l[1].startswith('http')]

        if len(internal_links) < 2:
            self.issues.append(SEOIssue(
                severity="info",
                category="links",
                message=f"內部連結數量偏少（{len(internal_links)} 個）",
                suggestion="建議加入 2-5 個相關文章的內部連結"
            ))

    def _check_images(self, markdown: str):
        """檢查圖片"""
        img_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        images = re.findall(img_pattern, markdown)

        # 檢查是否有圖片缺少 alt text
        for alt, src in images:
            if not alt.strip():
                self.issues.append(SEOIssue(
                    severity="warning",
                    category="images",
                    message=f"圖片缺少 alt 文字：{src}",
                    suggestion="所有圖片都應該有描述性的 alt 文字"
                ))

    def _calculate_score(self) -> int:
        """計算 SEO 分數"""
        base_score = 100

        for issue in self.issues:
            if issue.severity == "error":
                base_score -= 15
            elif issue.severity == "warning":
                base_score -= 5
            elif issue.severity == "info":
                base_score -= 2

        return max(0, min(100, base_score))

    def _get_stats(self, markdown: str, metadata: Dict) -> Dict:
        """取得統計資訊"""
        # 計算字數
        text = re.sub(r'```[\s\S]*?```', '', markdown)
        text = re.sub(r'[#*`\[\]()>-]', '', text)
        text = re.sub(r'\s+', '', text)
        word_count = len(text)

        # 計算標題數
        h2_count = len(re.findall(r'^## .+$', markdown, re.MULTILINE))
        h3_count = len(re.findall(r'^### .+$', markdown, re.MULTILINE))

        # 計算連結數
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        links = re.findall(link_pattern, markdown)

        return {
            'title_length': len(metadata.get('title', '')),
            'description_length': len(metadata.get('description', '')),
            'word_count': word_count,
            'h2_count': h2_count,
            'h3_count': h3_count,
            'link_count': len(links),
            'image_count': len(re.findall(r'!\[', markdown))
        }

    def _truncate_title(self, title: str) -> str:
        """截斷標題"""
        if len(title) <= self.TITLE_RECOMMENDED_MAX:
            return title

        # 在合適位置截斷
        truncated = title[:self.TITLE_RECOMMENDED_MAX - 3]
        # 找到最後一個完整的詞/符號
        for sep in ['｜', '|', '：', ':', '—', '-', ' ']:
            idx = truncated.rfind(sep)
            if idx > 20:
                return truncated[:idx] + '...'
        return truncated + '...'

    def _truncate_description(self, desc: str) -> str:
        """截斷描述"""
        if len(desc) <= self.DESC_RECOMMENDED_MAX:
            return desc

        truncated = desc[:self.DESC_RECOMMENDED_MAX - 3]
        # 找到最後一個句號
        idx = truncated.rfind('。')
        if idx > 50:
            return truncated[:idx + 1]
        return truncated + '...'

    def _add_internal_links(self, markdown: str, metadata: Dict) -> str:
        """添加內部連結建議（佔位符）"""
        # 這裡可以根據關鍵詞自動添加相關文章連結
        # 目前返回原內容，未來可以擴展
        return markdown


def analyze_seo(markdown: str, metadata: Dict) -> Dict:
    """便捷函式：分析 SEO"""
    optimizer = SEOOptimizer()
    return optimizer.analyze(markdown, metadata)


def optimize_content(markdown: str, metadata: Dict) -> Tuple[str, Dict]:
    """便捷函式：優化內容"""
    optimizer = SEOOptimizer()
    return optimizer.optimize(markdown, metadata)


if __name__ == "__main__":
    # 測試
    test_markdown = """---
title: "測試標題"
description: "測試描述"
---

# 這是 H1 標題

## 第一節

這是內容...

## 第二節

這是更多內容...

### 子標題

更多內容...
"""

    test_metadata = {
        'title': '這是一個非常非常非常非常非常非常非常非常非常非常長的測試標題',
        'description': '短描述',
        'keywords': ['測試', '關鍵詞']
    }

    optimizer = SEOOptimizer()
    result = optimizer.analyze(test_markdown, test_metadata)

    print(f"SEO 分數: {result['score']}")
    print(f"統計: {result['stats']}")
    print(f"\n問題列表:")
    for issue in result['issues']:
        print(f"  [{issue.severity}] {issue.category}: {issue.message}")
        print(f"          建議: {issue.suggestion}")
