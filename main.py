from loaders.pdf_loader import PDFLoader
from splitters.splitter import Splitter
from embeddings.embedding import Embeddings
from embeddings.vector_storage import VectorStorage
from graph.graph_builder import BuildingGraph
from graph.neo4j_store import Neo4jStorage
import logging
import asyncio

from dotenv import load_dotenv #type:ignore
load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    filename='app.log',
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def main():
    pdfloader = PDFLoader()
    splitter = Splitter()
    embeddings = Embeddings()
    vector = VectorStorage()
    graph = BuildingGraph()
    neo4j_storage = Neo4jStorage()
    pdf_path = r"C:\Users\91801\Downloads\gemini-code-1784740274787.pdf"
    logger.info(f"Initilization started with file path {pdf_path}")

# 1. Load
    response_from_pdf = pdfloader.pdf_loader(pdf_path)
    logger.info(f"Final response from pdf loader is \n=============> {response_from_pdf}")

# 2. Split
    response_from_splitter = splitter.split(response_from_pdf)
    logger.info(f"Final response from splitter \n=============> {response_from_splitter}")

# 3a. Embed
    response_from_embeddings = embeddings.generate_embeddings(response_from_splitter,100)
    logger.info(f"Final response from embeddings is \n=============> {response_from_embeddings}")
    
# 3b. Vector_storage
    respone_from_vector_storage = await vector.vector_storage(response_from_embeddings)
    logger.info(f"Final response from embeddings is \n=============> {respone_from_vector_storage}")    
    
# 4. Graph
    response_from_graph = graph.graph_building(response_from_splitter)
    logger.info(f"Final response from graph is \n=============> {response_from_graph}")
    
# 5. Neo4j storage

    respone_from_neo4jStorage = neo4j_storage.store(response_from_graph)
    logger.info(f"Final response from graph is \n=============> {respone_from_neo4jStorage}") 
    
    
    
if __name__ == "__main__":
    asyncio.run(main())

