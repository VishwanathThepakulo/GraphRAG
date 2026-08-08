# from embeddings.embedding import Embeddings 
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, PyMongoError
import logging
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from sentence_transformers import CrossEncoder



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
        embedding_api_key = os.getenv("EMBEDDING_API_KEY")
        if not embedding_api_key:
            raise ValueError("embedding api key not found")
        self.client = MongoClient(connection_string, serverSelectionTimeoutMS=2000)
        self.collection = self.client['RAG_Collection']['Searchable_TABLE']
        self.embedding_model = HuggingFaceEndpointEmbeddings(
            model="sentence-transformers/all-MiniLM-L6-v2",
            huggingfacehub_api_token=embedding_api_key,
        )
        self.reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-12-v2')

    def query_embedding(self, query):
        embedded_query = self.embedding_model.embed_query(query)
        return embedded_query
    
    def similarity_search(self, embedded_query):
        if not embedded_query or not isinstance(embedded_query, list):
            raise ValueError("embedded_query must be a non-empty list of floats")
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "embeddings",
                    "queryVector": embedded_query,
                    "numCandidates": 100,
                    "limit": 5
                }
            },
            {
                "$project":{
                "_id": 0,
                "text": 1,
                "metadata": 1,
                "score": {"$meta": "vectorSearchScore"},  
                }
            }
        ]
        
        try:
            result = list(self.collection.aggregate(pipeline))
        except PyMongoError as e:
            logger.error("Vector search failed: %s", e)
            raise RuntimeError("Similarity search failed") from e
        
        parts = []
        for doc in result:
            text = doc.get('text', '')
            if text:
                parts.append(text)
        context = "\n\n".join(parts)
        
        return {
            'document' : result,
            'context' : context,
            'count' : len(result)
        }
        
def main():
    vector = VectorRetrievr()
    query_output = vector.query_embedding("who introduced transformer model")
    similarity_output = vector.similarity_search(query_output)
    print(similarity_output)
    
if __name__ == "__main__":
    main()












