
import urllib.request
import urllib.error
import re
from html.parser import HTMLParser
from typing import List, Dict, Any
import sys
import os

# Add parent directory to path to import state
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from state import PageData

class SimpleHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h_structure = []
        self.current_tag = ""
        self.title = ""
        self.meta_description = ""
        self.text_content = []
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        if tag in ['h1', 'h2', 'h3']:
            self.h_structure.append({'tag': tag, 'text': ''})
        elif tag == 'title':
            self.in_title = True
        elif tag == 'meta':
            attrs_dict = dict(attrs)
            if attrs_dict.get('name') == 'description':
                self.meta_description = attrs_dict.get('content', '')

    def handle_endtag(self, tag):
        self.current_tag = ""
        if tag == 'title':
            self.in_title = False

    def handle_data(self, data):
        clean_data = data.strip()
        if not clean_data:
            return
            
        if self.in_title:
            self.title = clean_data
            
        if self.h_structure and self.h_structure[-1]['tag'] == self.current_tag:
             # Append to the current header (handling nested tags logic roughly)
            self.h_structure[-1]['text'] += clean_data + " "
            
        # Collect all text for word count
        self.text_content.append(clean_data)

def crawl_url(url: str) -> Dict[str, Any]:
    """
    Fetches content from a URL and returns a PageData-compatible dictionary using standard libraries.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8', errors='ignore')
            
        parser = SimpleHTMLParser()
        parser.feed(content)
        
        # Clean up header text
        clean_structure = []
        for h in parser.h_structure:
            clean_structure.append({
                'tag': h['tag'],
                'text': h['text'].strip()
            })
            
        word_count = len("".join(parser.text_content))
        
        return {
            'url': url,
            'title': parser.title,
            'meta_description': parser.meta_description,
            'word_count': word_count,
            'h_structure': clean_structure
        }
        
    except Exception as e:
        print(f"Error crawling {url}: {e}", file=sys.stderr)
        return None

def run_crawler(urls: List[str]) -> List[PageData]:
    results = []
    print(f"Crawler started. Processing {len(urls)} URLs...")
    for url in urls:
        data = crawl_url(url)
        if data:
            results.append(PageData(**data))
    return results

if __name__ == "__main__":
    # Test block
    test_urls = ["https://max.maicoin.com/", "https://www.bitopro.com/"]
    data = run_crawler(test_urls)
    print(f"Successfully crawled {len(data)} pages.")
    for p in data:
        print(f"- {p.title} ({p.word_count} chars)")
