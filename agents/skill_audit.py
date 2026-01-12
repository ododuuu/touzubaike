import re
import os
import json

class SEOAuditor:
    def __init__(self, file_path, keyword):
        self.file_path = file_path
        self.keyword = keyword
        self.content = ""
        self.frontmatter = {}
        self.body = ""
        self.report = {
            "passed": False,
            "score": 0,
            "checks": []
        }

    def load_file(self):
        with open(self.file_path, "r", encoding="utf-8") as f:
            self.content = f.read()
            
        # 簡單分離 Frontmatter 與 Body
        parts = self.content.split("---")
        if len(parts) >= 3:
            # 簡單解析 YAML (不依賴 PyYAML 以減少依賴)
            yaml_text = parts[1]
            for line in yaml_text.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    self.frontmatter[key.strip()] = value.strip().strip('"').strip("'")
            self.body = "---".join(parts[2:])
        else:
            self.body = self.content

    def check_title(self):
        title = self.frontmatter.get("title", "")
        check = {
            "name": "Title Keyword Check",
            "status": "fail",
            "message": ""
        }
        
        if self.keyword in title:
            check["status"] = "pass"
            check["message"] = f"標題包含關鍵字 '{self.keyword}'"
            self.report["score"] += 20
        else:
            check["message"] = f"標題未包含關鍵字 '{self.keyword}'"
            
        self.report["checks"].append(check)

    def check_first_200_words(self):
        # 取前 500 個字元 (約等於中文 200-300 字)
        start_content = self.body[:500]
        count = start_content.count(self.keyword)
        
        check = {
            "name": "First 200 Words Keyword Density",
            "status": "fail",
            "message": ""
        }
        
        if count >= 2:
            check["status"] = "pass"
            check["message"] = f"前段內容出現關鍵字 {count} 次 (標準: >= 2)"
            self.report["score"] += 20
        else:
            check["message"] = f"前段內容僅出現關鍵字 {count} 次 (建議增加)"
            
        self.report["checks"].append(check)

    def check_structure(self):
        h2_count = len(re.findall(r"^##\s", self.body, re.MULTILINE))
        h3_count = len(re.findall(r"^###\s", self.body, re.MULTILINE))
        
        check = {
            "name": "Heading Structure",
            "status": "fail",
            "message": ""
        }
        
        if h2_count >= 2:
            check["status"] = "pass"
            check["message"] = f"結構良好 (H2: {h2_count}, H3: {h3_count})"
            self.report["score"] += 20
        else:
            check["message"] = f"文章結構過於單薄 (H2 只有 {h2_count} 個)"
            
        self.report["checks"].append(check)

    def check_links(self):
        # 簡單檢查是否有連結語法 [text](url)
        links = re.findall(r"\[.*?\]\((.*?)\)", self.body)
        external_links = [l for l in links if l.startswith("http")]
        internal_links = [l for l in links if not l.startswith("http") and not l.startswith("#")]
        
        check_ext = {
            "name": "External Links",
            "status": "pass" if len(external_links) >= 1 else "warning",
            "message": f"外部連結: {len(external_links)} 個"
        }
        self.report["score"] += 10 if len(external_links) >= 1 else 0
        
        check_int = {
            "name": "Internal Links",
            "status": "pass" if len(internal_links) >= 1 else "warning",
            "message": f"內部連結: {len(internal_links)} 個"
        }
        self.report["score"] += 10 if len(internal_links) >= 1 else 0
        
        self.report["checks"].append(check_ext)
        self.report["checks"].append(check_int)

    def check_word_count(self):
        # 簡單估算字數 (中文字)
        # 移除 markdown 符號
        text_only = re.sub(r"[#\*\-\[\]\(\)]", "", self.body)
        word_count = len(text_only.replace(" ", "").replace("\n", ""))
        
        check = {
            "name": "Word Count",
            "status": "pass" if word_count >= 1500 else "fail",
            "message": f"預估字數: {word_count} (標準: > 1500)"
        }
        
        if word_count >= 1500:
            self.report["score"] += 20
        
        self.report["checks"].append(check)

    def run_audit(self):
        self.load_file()
        self.check_title()
        self.check_first_200_words()
        self.check_structure()
        self.check_links()
        self.check_word_count()
        
        self.report["passed"] = self.report["score"] >= 80
        return self.report

if __name__ == "__main__":
    # 測試
    target_file = "src/content/blog/usdt-complete-guide-2026.md"
    keyword = "USDT" # 注意大小寫，或在程式中做正規化
    
    # 因為關鍵字可能是 "usdt是什麼"，但文章標題是 "USDT是什麼"
    # 這裡簡單處理：檢查關鍵字是否在標題內，不區分大小寫
    
    auditor = SEOAuditor(target_file, "USDT")
    report = auditor.run_audit()
    
    print(json.dumps(report, ensure_ascii=False, indent=2))
