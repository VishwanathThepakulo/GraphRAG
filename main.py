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


async def vector_branch(embeddings, vector, chunk):
    loop = asyncio.get_running_loop()
    docs = await loop.run_in_executor(
        None,
        embeddings.generate_embeddings,
        chunk,
        100 ,
    )
    return await vector.vector_storage(docs)


async def graph_branch(graph, neo4j_storage, chunk):
    loop = asyncio.get_running_loop()
    graph_docs = await loop.run_in_executor(
        None, 
        graph.graph_building,
        chunk,
    )
    storage_result = await loop.run_in_executor(
        None,
        neo4j_storage.store,
        graph_docs,
    )
    return storage_result
    

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

# # 3a. Embed
#     response_from_embeddings = embeddings.generate_embeddings(response_from_splitter,100)
#     logger.info(f"Final response from embeddings is \n=============> {response_from_embeddings}")
    
# # 3b. Vector_storage
#     respone_from_vector_storage = await vector.vector_storage(response_from_embeddings)
#     logger.info(f"Final response from embeddings is \n=============> {respone_from_vector_storage}")    
    
# # 4a. Graph
#     response_from_graph = graph.graph_building(response_from_splitter)
#     logger.info(f"Final response from graph is \n=============> {response_from_graph}")
    
# # 4b. Neo4j storage

#     respone_from_neo4jStorage = neo4j_storage.store(response_from_graph)
#     logger.info(f"Final response from graph is \n=============> {respone_from_neo4jStorage}") 

    vector_result, graph_result = await asyncio.gather(
        vector_branch(embeddings, vector, response_from_splitter),
        graph_branch(graph, neo4j_storage, response_from_splitter)
    )
    logger.info(f"Response from vector result is \n=============>{vector_result}")
    logger.info(f"Response from graph result is \n=============>{graph_result}")
    
if __name__ == "__main__":
    asyncio.run(main())

