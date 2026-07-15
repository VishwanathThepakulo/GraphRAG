from langchain_text_splitters import RecursiveCharacterTextSplitter
from lang
import logging

logger = logging.getLogger(__name__)


class Splitter:
    def chunking(self, docs_to_split:list)->list:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 500,
            chunk_overlap = 100,
            separators=["\n\n", "\n", " ", ""], 
            add_start_index=True,
        )
        docs = text_splitter.split_documents(docs_to_split)
        
        
        ...