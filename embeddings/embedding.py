from langchain_huggingface import HuggingFaceEndpointEmbeddings
from dotenv import load_dotenv
from langchain_core.documents import Document #type:ignore
import logging
import os
import time
load_dotenv()

logger = logging.getLogger(__name__)

class Embeddings:
    def __init__(self):
        embedding_api_key = os.getenv('EMBEDDING_API_KEY')
        if not embedding_api_key:
            raise ValueError("APIKey not found for Embeddings")
        self.embedding_model = HuggingFaceEndpointEmbeddings(
            model="sentence-transformers/all-MiniLM-L6-v2",
            huggingfacehub_api_token=embedding_api_key,
        )
        
        
    def generate_embeddings(self, documents: list[Document], batch_size: int=50) -> list[dict]:
        if not documents:
            return []
        texts = [doc.page_content for doc in documents]
        max_retry = 3
        all_embeddings = []
        for i in range(0,len(texts),batch_size):
            batch_text = texts[i:i+batch_size]
            batch_embeddings = None
            for retry in range(max_retry):
                try:
                    batch_embeddings = self.embedding_model.embed_documents(batch_text)
                    # print(batch_embeddings[0])
                    # print(type(batch_embeddings))
                    logger.info(
                        "Generated embeddings for %d chunks",
                        len(batch_text)
                    )
                    break
                except Exception as e:
                    logger.warning(f"Embeddings attempt {retry+1} failed : {e}")
                    if retry<max_retry-1:
                        time.sleep(2**retry)
                    else:
                        raise RuntimeError("Embedding generation failed")
            if batch_embeddings:
                all_embeddings.extend(batch_embeddings)
        logger.info("Successfully generated embeddings for %d chunks", len(texts))
        result = []
   
        for doc, vector in zip(documents,all_embeddings):
            result.append({
                "text":doc.page_content,
                "embedding":vector,
                "metadata":doc.metadata
                })
        return result 