from langchain_huggingface import HuggingFaceEndpointEmbeddings
# from dotenv import load_dotenv
from langchain_core.documents import Document #type:ignore
import logging
import os
import time
# load_dotenv()

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
        
        
    def generate_embeddings(self, documents: list[Document]) -> list[dict]:
        texts = [doc.page_content for doc in documents]
        max_retry = 3
        embeddings = None
        for retry in range(max_retry):
            try:
                embeddings = self.embedding_model.embed_documents(texts)
                logger.info(
                    "Generated embeddings for %d chunks",
                    len(texts)
                )
                break
            except Exception as e:
                logger.warning(f"Embeddings attempt {retry+1} failed : {e}")
                if retry<max_retry-1:
                    time.sleep(2**retry)
                else:
                    raise RuntimeError("Embedding generation failed")
        result = []
        if embeddings:
            for doc, vector in zip(documents,embeddings):
                result.append({
                    "text":doc.page_content,
                    "embedding":vector,
                    "metadata":doc.metadata
                })
            return result 