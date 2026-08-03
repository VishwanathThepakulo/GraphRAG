from embeddings.embedding import Embeddings 
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, PyMongoError
import logging
from langchain_huggingface import HuggingFaceEndpointEmbeddings



load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class VectorRetrievr():
    def __init__(self):    
        connection_string = os.getenv("DB_CREDENTIALS")
        if not connection_string:
            raise ValueError("Connection string not found")
        self.client = MongoClient(connection_string, serverSelectionTimeoutMS=2000)
        self.collection = self.client['RAG_Collection']['Searchable_TABLE']
        self.embedding_model = HuggingFaceEndpointEmbeddings(
            model="sentence-transformers/all-MiniLM-L6-v2",
            huggingfacehub_api_token=embedding_api_key,
        )
        self.reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-12-v2')



