from langchain_huggingface import HuggingFaceEndpointEmbeddings
# from dotenv import load_dotenv
import logging
import os
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
        
        
    def embeddings(self, chunks_to_embed):
        self.embedding_model(chunks_to_embed)
        ...