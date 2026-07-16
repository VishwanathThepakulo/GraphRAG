from langchain_docling.loader import DoclingLoader # type: ignore
from langchain_core.documents import Document # type: ignore
import logging

logging.basicConfig(
    level=logging.INFO,
    # filename='app.log',
    # filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class PDFLoader:
    def pdf_loader(self, file_path: str) -> list[Document]:
        try:
            loader = DoclingLoader(file_path=file_path)        
            document = loader.load()
            logger.info(f"==========>\n Document loaded successfully {len(document)}")
            return document
        except Exception as e:
            logger.error(f"=============> \n Document loading failed and error is \n {e}")
            raise RuntimeError("Unable to load PDF")
            
if __name__ == "__main__":
    pdfloader = PDFLoader()
    pdf_path = r"C:/Users/91801/Downloads/LangChain.pdf"
    logger.info(f"Initilization started with file path {pdf_path}")
    response = pdfloader.pdf_loader(pdf_path)
    logger.info(f"Final response is \n=============> {response}")
    
            



