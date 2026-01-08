
import sys
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def crawl_url(url):
    """
    Fetches the content of a URL and extracts SEO-relevant data.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract H-tags
        h_structure = []
        for header in soup.find_all(['h1', 'h2', 'h3']):
            h_structure.append({
                'tag': header.name,
                'text': header.get_text(strip=True)
            })
            
        # Estimate word count (naive)
        text_content = soup.get_text(separator=' ', strip=True)
        word_count = len(text_content) # Character count for Chinese
        
        # Meta description
        meta_desc = ""
        meta_tag = soup.find('meta', attrs={'name': 'description'})
        if meta_tag:
            meta_desc = meta_tag.get('content')
            
        return {
            'url': url,
            'title': soup.title.string if soup.title else "",
            'meta_description': meta_desc,
            'word_count': word_count,
            'h_structure': h_structure,
            'status': 'success'
        }
        
    except Exception as e:
        return {
            'url': url,
            'status': 'error',
            'error': str(e)
        }

def main():
    if len(sys.argv) < 2:
        print("Usage: python crawler_skill.py <url1> <url2> ...")
        sys.exit(1)
        
    urls = sys.argv[1:]
    results = []
    
    print(f"Crawling {len(urls)} URLs...")
    for url in urls:
        result = crawl_url(url)
        results.append(result)
        
    # Output JSON to stdout for the Agent to capture
    print(json.dumps(results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
