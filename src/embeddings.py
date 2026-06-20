from langchain_openai import OpenAIEmbeddings
from src.config import Config
from dotenv import load_dotenv
import os

load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')

class EmbeddingManager:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model=Config.EMBEDDING_MODEL,
            openai_api_key=Config.OPENAI_API_KEY
        )
    
    def get_embeddings(self):
        return self.embeddings