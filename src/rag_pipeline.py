from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from typing import List, Tuple, Dict, Any
from src.config import Config
from src.vector_store import VectorStoreManager
from dotenv import load_dotenv

load_dotenv(override=True)

class RAGPipeline:
    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=Config.TEMPERATURE,
            model=Config.LLM_MODEL,
            openai_api_key=Config.OPENAI_API_KEY
        )
        self.vector_manager = VectorStoreManager()
        self.retriever = None
    
    def initialize_retriever(self):
        """Initialize the retriever from existing vector store."""
        self.retriever = self.vector_manager.get_retriever()
    
    def query(self, question: str, top_k: int = Config.TOP_K) -> Tuple[str, List[Dict[str, Any]], bool]:
        """
        Process a query through the RAG pipeline.
        
        Returns:
            answer: The generated answer
            sources: List of source chunks with metadata
            found_answer: Boolean indicating if answer was found
        """
        if self.retriever is None:
            self.initialize_retriever()

        if self.retriever is None:
            raise RuntimeError("Retriever failed to initialize.")
        
        docs = self.retriever.invoke(question)
        
        context = "\n\n---\n\n".join(doc.page_content for doc in docs)
        
        system_prompt = Config.SYSTEM_PROMPT.format(context=context)
        
        response = self.llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=question)
        ])
        
        answer = response.content
        if not isinstance(answer, str):
            answer = str(answer)
        
        found_answer = "I'm sorry, but I cannot find that information" not in answer
        
        sources = [
            {
                "content": doc.page_content,
                "metadata": doc.metadata
            }
            for doc in docs
        ]
        
        return answer, sources, found_answer