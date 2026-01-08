
from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class SectionState:
    id: str
    h2_title: str
    h3_subsections: List[str]
    key_points: List[str]
    target_length: int
    draft_content: Optional[str] = None
    review_score: int = 0
    review_feedback: List[str] = field(default_factory=list)
    status: str = "planned" # planned, drafted, reviewed, approved

@dataclass
class MasterOutline:
    title: str
    description: str
    target_word_count: int
    sections: List[SectionState]

@dataclass
class PageData:
    url: str
    title: str
    meta_description: str
    word_count: int
    h_structure: List[Dict[str, str]] # [{'tag': 'h2', 'text': '...'}, ...]

@dataclass
class CompetitorAnalysis:
    top_urls: List[str]
    avg_word_count: int
    common_topics: List[str]
    gap_topics: List[str]

@dataclass
class ArticleState:
    keyword: str
    research_data: Optional[CompetitorAnalysis] = None
    outline: Optional[MasterOutline] = None
    current_section_index: int = 0
    status: str = "initialized" # initialized, researching, planning, writing, deploying, done
