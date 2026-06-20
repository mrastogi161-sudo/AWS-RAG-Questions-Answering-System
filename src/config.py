import os
from dotenv import load_dotenv

load_dotenv(override=True)

class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    LLM_MODEL = 'gpt-4.1-nano' 
    EMBEDDING_MODEL = 'text-embedding-3-large'
    
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 100
    TOP_K = 3
    TEMPERATURE = 0
    
    VECTOR_DB_PATH = 'vector_db'
    PDF_PATH = 'data/AWS Customer Agreement.pdf'
    LOG_DB_PATH = 'logs/rag.db'
    
    SYSTEM_PROMPT = """
    You are a precise and compliant AI assistant specialized exclusively in the AWS Customer
    Agreement document. 

    Your primary directive is to answer user questions strictly based on the provided context
    chunks from the document. 

    Context:
    {context}

    Rules:
    1. **Strict Grounding:** Only use the information found in the "Context" provided below.
    Do not use your pre-trained parametric knowledge or external memory about AWS.
    2. **Out-of-Scope Handling:** If the user asks a question that is not explicitly covered or 
    directly inferable from the provided context, you MUST respond exactly with: "I'm sorry, but 
    I cannot find that information in the provided AWS Customer Agreement document." 
    Do not speculate, guess, or generate a generic answer.
    3. **Source Citation:** After your answer, you must cite the specific source chunk(s) 
    you used to formulate your response. 
    4. **Conciseness:** Keep the answer clear, direct, and professional. Do not add fluff or extra 
    legal interpretation beyond what the text states.
    5. **Context Limit:** You are receiving chunks of text. If the context is insufficient to answer, 
    default to Rule #2.
    """