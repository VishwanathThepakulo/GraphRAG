from langchain_community.graphs import Neo4jGraph
import os
from dotenv import load_dotenv

load_dotenv()

class Neo4jStorage():
    def __init__(self):
        url = os.getenv("NEO4J_URI")
        username = os.getenv("NEO4J_USERNAME")
        password = os.getenv("NEO4J_PASSWORD")
        # database = os.getenv("NEO4J_DATABASE")
        # instance = os.getenv("AURA_INSTANCEID")
        # instance_name = os.getenv("AURA_INSTANCENAME")
        
        self.graph = Neo4jGraph(
            url = url,
            username = username,
            password = password
        )
        
        
    def store(self, graph_document):
        result = self.graph.add_graph_documents(graph_document)
        return result
    
    def test_connection(self):
        return self.graph.query("Return 1 as ok")
    
    def verify(self):
        nodes = self.graph.query("MATCH (n) RETURN count(n) AS node_count")
        rels = self.graph.query("MATCH ()-[r]->() RETURN count(r) AS rel_count")
        return {"nodes": nodes[0]["node_count"], "relationships": rels[0]["rel_count"]}
    
    
    
if __name__=="__main__":
    storage = Neo4jStorage()
    result = storage.test_connection()
    print(result)
    verify = storage.verify()
    print(verify)
