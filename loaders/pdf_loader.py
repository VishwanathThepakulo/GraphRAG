from langchain_docling.loader import DoclingLoader # type: ignore
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class PdfLoader:
    def pdf_loader(self, file_path: str):
        loader = DoclingLoader(file_path=file_path)        
        document = loader.load()
        loader.info(f"==========> {len(document)}")
        return document



