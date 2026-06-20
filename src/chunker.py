from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List
from langchain_core.documents import Document
from src.config import Config

class DocumentChunker:
    def __init__(self, chunk_size: int = Config.CHUNK_SIZE, 
                 chunk_overlap: int = Config.CHUNK_OVERLAP):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks."""
        return self.text_splitter.split_documents(documents)