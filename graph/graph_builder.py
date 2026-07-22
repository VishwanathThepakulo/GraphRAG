from langchain_experimental.graph_transformers import LLMGraphTransformer

from langchain_community.graphs import Neo4jGraph

from langchain_core.documents import Document

from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os
load_dotenv()



# Defined Schema tailored for Academic & AI Literature
allowed_nodes = [
    "Author",  # e.g., Ashish Vaswani, Noam Shazeer
    "Organization",  # e.g., Google Brain, Google Research, University of Toronto
    "Model",  # e.g., Transformer, RNN, LSTM, Convolutional Neural Network
    "Component",  # e.g., Multi-Head Attention, Encoder, Decoder, Positional Encoding
    "Concept",  # e.g., Self-Attention, Parallelization, Scaled Dot-Product Attention
    "Dataset",  # e.g., WMT 2014 English-to-German, WMT 2014 English-to-French
    "Metric",  # e.g., BLEU Score, Training Cost
]

allowed_relationships = [
    "AUTHORED_BY",  # Paper/Model -> Author
    "AFFILIATED_WITH",  # Author -> Organization
    "INTRODUCES",  # Paper -> Model/Concept
    "CONSISTS_OF",  # Model -> Component
    "USES_MECHANISM",  # Component -> Concept
    "REPLACES",  # Model -> Model (e.g., Transformer REPLACES RNN)
    "EVALUATED_ON",  # Model -> Dataset
    "MEASURED_BY",  # Model -> Metric
]



class BuildingGraph():
    def __init__(self):
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            raise ValueError("LLM api key not found")
        self.model = init_chat_model(
            model='openai/gpt-oss-120b',
            model_provider='groq',
            api_key = api_key,
            temperature=0.1,
        )    
    
    
    
    
    
    def graph_building(self, documents:list[Document])->list[Document]:
    # def graph_building(self, doc):
        transformer = LLMGraphTransformer(
            llm = self.model,
            allowed_nodes=allowed_nodes,
            allowed_relationships=allowed_relationships,
            node_properties=["name", "description"],
            strict_mode=True
        )
        graph_documents = transformer.convert_to_graph_documents(documents)
        print("Nodes:", graph_documents[0].nodes)
        print("Relationships:", graph_documents[0].relationships)
        
        return graph_documents
        
        
        
if __name__=="__main__":
    doc = Document(
        page_content="Sam Altman is the CEO of OpenAI, which is headquartered in San Francisco."
    )
    builder = BuildingGraph()
    builder.graph_building(doc)


    
# 3. Create sample document
# doc = Document(
#     page_content="Sam Altman is the CEO of OpenAI, which is headquartered in San Francisco."
# )

# # 4. Transform text into Graph Documents
# graph_documents = llm_transformer.convert_to_graph_documents([doc])

# # Inspect output
# print("Nodes:", graph_documents[0].nodes)
# print("Relationships:", graph_documents[0].relationships)
