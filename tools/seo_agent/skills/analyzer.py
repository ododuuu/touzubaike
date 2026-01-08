
from typing import List, Dict
import sys
import os
import statistics
from collections import Counter
import re

# Add parent directory to path to import state
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from state import PageData, CompetitorAnalysis

def extract_keywords(text: str) -> List[str]:
    # Very basic keyword extraction for demo purposes
    # unique words > 2 chars
    words = re.findall(r'\w+', text)
    return [w for w in words if len(w) > 1]

def run_analyzer(pages: List[PageData]) -> CompetitorAnalysis:
    if not pages:
        return CompetitorAnalysis([], 0, [], [])

    # 1. Calculate Average Word Count
    word_counts = [p.word_count for p in pages]
    avg_count = int(statistics.mean(word_counts)) if word_counts else 0
    
    # 2. Identify Common Topics (H2 headers)
    # We collect all H2 texts
    all_h2s = []
    for p in pages:
        for h in p.h_structure:
            if h['tag'] == 'h2':
                all_h2s.append(h['text'])
    
    # Simple frequency analysis to find common themes
    # In a real agent, this would use an LLM or vector embeddings
    # Here we just list the top recurring phrases/keywords in headers
    
    # Mocking "Common Topics" for now based on H2s
    # In production, we'd cluster these semantically
    common_topics = all_h2s # Return all for the LLM to process later
    
    # 3. Identify Gap Topics
    # This usually requires comparison with a "Knowledge Base" or user query data
    # For this skill, we'll leave it empty to be filled by the LLM (Outliner) 
    # who can compare what's here vs what SHOULD be here
    gap_topics = [] 

    return CompetitorAnalysis(
        top_urls=[p.url for p in pages],
        avg_word_count=avg_count,
        common_topics=common_topics,
        gap_topics=gap_topics
    )

if __name__ == "__main__":
    # Test block
    pass
