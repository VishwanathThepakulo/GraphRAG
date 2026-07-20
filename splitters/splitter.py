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
        split_documents = text_splitter.split_documents(documents)
        logger.info("Created %d chunks", len(split_documents))
        # logger.info(f"docs from text splitter is \n===================> {split_documents}")
        for chunk_index, doc in enumerate(split_documents):
            doc.metadata["chunk_index"] = chunk_index
            source = doc.metadata.get('source', 'unknown')
            page = doc.metadata.get('page', 0)
            doc.metadata["chunk_id"] = (
                f"{source}_page_{page}_chunk_{chunk_index}"
            )
        return split_documents
        
# if __name__=="__main__":
#     splitter = Splitter()
#     splitter.split()





