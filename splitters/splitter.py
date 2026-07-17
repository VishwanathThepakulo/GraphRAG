from langchain_text_splitters import RecursiveCharacterTextSplitter#type:ignore
from langchain_core.documents import Document#type:ignore
import logging

logger = logging.getLogger(__name__)


class Splitter:
    def split(self, documents: list[Document]) -> list[Document]:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 500,
            chunk_overlap = 100,
            separators=["\n\n", "\n", " ", ""], 
            add_start_index=True,
        )
        docs = text_splitter.split_documents(documents)
        logger.info("Created %d chunks", len(docs))
        logger.info(f"docs from text splitter is \n===================> {docs}")
        return docs
        
# if __name__=="__main__":
#     splitter = Splitter()
#     splitter.split()





