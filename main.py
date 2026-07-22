from loaders.pdf_loader import PDFLoader
from splitters.splitter import Splitter
from embeddings.embedding import Embeddings
from graph.graph_builder import BuildingGraph
import logging
from dotenv import load_dotenv
load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    filename='app.log',
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    pdfloader = PDFLoader()
    splitter = Splitter()
    embeddings = Embeddings()
    graph = BuildingGraph()
    pdf_path = r"C:\Users\91801\Downloads\gemini-code-1784740274787.pdf"
    logger.info(f"Initilization started with file path {pdf_path}")

# 1. Load
    response_from_pdf = pdfloader.pdf_loader(pdf_path)
    logger.info(f"Final response from pdf loader is \n=============> {response_from_pdf}")

# 2. Split
    response_from_splitter = splitter.split(response_from_pdf)
    logger.info(f"Final response from splitter \n=============> {response_from_splitter}")

# 3. Embed
    response_from_embeddings = embeddings.generate_embeddings(response_from_splitter,100)
    logger.info(f"Final response from embeddings is \n=============> {response_from_embeddings}")
    
# 4. Graph
    response_from_graph = graph.graph_building(response_from_splitter)
    logger.info(f"Final response from graph is \n=============> {response_from_graph}")
if __name__ == "__main__":
    main()


# import logging
# from dotenv import load_dotenv

# # Load variables before executing main classes
# load_dotenv()

# from embeddings.embedding import Embeddings
# from loaders.pdf_loader import PDFLoader
# from splitters.splitter import Splitter

# logging.basicConfig(
#     level=logging.INFO,
#     filename="app.log",
#     filemode="w",
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
# )

# logger = logging.getLogger(__name__)


# def main():
#     pdfloader = PDFLoader()
#     splitter = Splitter()
#     embeddings = Embeddings()

#     pdf_path = r"C:\Users\91801\Downloads\LangChain.pdf"
#     logger.info(f"Initialization started with file path: {pdf_path}")

#     # 1. Load
#     response_from_pdf = pdfloader.pdf_loader(pdf_path)

#     # 2. Split
#     response_from_splitter = splitter.split(response_from_pdf)

#     # 3. Embed
#     response_from_embeddings = embeddings.generate_embeddings(
#         response_from_splitter, batch_size=50
#     )

#     logger.info(
#         "Pipeline complete! Output contains %d structured dictionary records.",
#         len(response_from_embeddings),
#     )


# if __name__ == "__main__":
#     main()