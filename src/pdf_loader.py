from langchain_community.document_loaders import PyPDFLoader
from typing import List
from langchain_core.documents import Document

class PDFLoader:
    @staticmethod
    def load_pdf(pdf_path: str) -> List[Document]:
        """Load PDF and return documents."""
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        return documents