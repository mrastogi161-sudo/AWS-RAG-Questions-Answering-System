import os
from langchain_chroma import Chroma
from typing import List
from langchain_core.documents import Document
from src.config import Config
from src.embeddings import EmbeddingManager

class VectorStoreManager:
    def __init__(self, persist_directory: str = Config.VECTOR_DB_PATH):
        self.persist_directory = persist_directory
        self.embeddings = EmbeddingManager().get_embeddings()
        self.vectorstore = None
    
    def create_vectorstore(self, documents: List[Document]):
        """Create vector store from documents."""
        if os.path.exists(self.persist_directory):
            Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            ).delete_collection()
        
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        return self.vectorstore
    
    def load_vectorstore(self):
        """Load existing vector store."""
        if os.path.exists(self.persist_directory):
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
            return self.vectorstore
        raise FileNotFoundError("Vector store not found. Run ingestion first.")
    
    def get_retriever(self, search_kwargs: dict | None = None):
        """Get retriever from vector store."""
        if self.vectorstore is None:
            self.load_vectorstore()
        
        if search_kwargs is None:
            search_kwargs = {"k": Config.TOP_K}
        
        return self.vectorstore.as_retriever(search_kwargs=search_kwargs)