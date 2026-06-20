import sqlite3
import json
from datetime import datetime
from typing import Dict, Any, List
from src.config import Config
import os

class Database:
    def __init__(self, db_path: str = Config.LOG_DB_PATH):
        self.db_path = db_path
        self._ensure_directory_exists()
        self.init_db()
    def _ensure_directory_exists(self):
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
    
    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS query_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    sources TEXT NOT NULL,  -- JSON list of source chunks
                    found_answer BOOLEAN DEFAULT 1,
                    response_time_ms INTEGER NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    top_k INTEGER,
                    model_used TEXT
                )
            """)
    
    def log_query(self, query: str, answer: str, sources: List[Dict], 
                  found_answer: bool, response_time_ms: int, 
                  top_k: int = 3, model: str = Config.LLM_MODEL):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO query_logs 
                (query, answer, sources, found_answer, response_time_ms, top_k, model_used)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (query, answer, json.dumps(sources), found_answer, 
                  response_time_ms, top_k, model))
    
    def get_analytics(self) -> Dict[str, Any]:
        with sqlite3.connect(self.db_path) as conn:
            freq_queries = conn.execute("""
                SELECT query, COUNT(*) as count 
                FROM query_logs 
                GROUP BY query 
                ORDER BY count DESC 
                LIMIT 10
            """).fetchall()
            
            
            stats = conn.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN found_answer = 0 THEN 1 ELSE 0 END) as no_answer_count
                FROM query_logs
            """).fetchone()
            
           
            avg_latency = conn.execute("""
                SELECT AVG(response_time_ms) as avg_ms 
                FROM query_logs
            """).fetchone()
            
            total_queries = stats[0] if stats[0] else 0
            no_answer_count = stats[1] if stats[1] else 0
            
            return {
                "most_frequent_queries": [
                    {"question": q[0], "count": q[1]} 
                    for q in freq_queries
                ],
                "no_answer_rate": no_answer_count / total_queries if total_queries > 0 else 0,
                "total_queries": total_queries,
                "avg_response_latency_ms": round(avg_latency[0], 2) if avg_latency[0] else 0
            }