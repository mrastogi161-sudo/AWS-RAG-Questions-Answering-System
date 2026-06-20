from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class AskRequest(BaseModel):
    query: str
    top_k: Optional[int] = 3

class Source(BaseModel):
    content: str
    metadata: Dict[str, Any]

class AskResponse(BaseModel):
    query: str
    answer: str
    sources: List[Source]
    found_answer: bool
    response_time_ms: int

class AnalyticsResponse(BaseModel):
    most_frequent_queries: List[Dict[str, Any]]
    no_answer_rate: float
    total_queries: int
    avg_response_latency_ms: float