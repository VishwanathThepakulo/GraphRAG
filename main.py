from loaders.pdf_loader import PDFLoader
from splitters.splitter import Splitter
import logging

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
    pdf_path = r"C:\Users\91801\Downloads\LangChain.pdf"
    logger.info(f"Initilization started with file path {pdf_path}")
    response = pdfloader.pdf_loader(pdf_path)
    logger.info(f"Final response is \n=============> {response}")
    result = splitter.split(response)
    logger.info(f"Final response is \n=============> {result}")


if __name__ == "__main__":
    main()
