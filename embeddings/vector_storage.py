from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import logging


logger = logging.getLogger(__name__)



load_dotenv()

class VectorStorage:
    def __init__(self):
        db_credentials = os.getenv("DB_CREDENTIALS")
        if not db_credentials:
            raise ValueError("DB Credentials required")
        
        self.client = AsyncIOMotorClient(db_credentials)
        self.collection = self.client['Vector_for_graph_rag']['searchable_doc']
        
        
    async def vector_storage(self,docs_to_insert):
        try:
            result = await self.collection.insert_many(docs_to_insert)
            return {
                'status' : 200,
                "inserted_count":len(result.inserted_ids)
            }
        except Exception as e:
            logger.error("Vector storage failed: %s", e)
            raise RuntimeError("Unable to store vectors in MongoDB") from e



if __name__ == "__main__":
    vector = VectorStorage()









