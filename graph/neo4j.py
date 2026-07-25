from langchain_community.graphs import Neo4jGraph
import os
from dotenv import load_dotenv

load_dotenv()

class Neo4jStorage():
    def __init__(self):
        url = os.getenv("NEO4J_URI")
        username = os.getenv("NEO4J_USERNAME")
        password = os.getenv("NEO4J_PASSWORD")
        database = os.getenv("NEO4J_DATABASE")
        instance = os.getenv("AURA_INSTANCEID")
        instance_name = os.getenv("AURA_INSTANCENAME")
        
        self.Neo4jGraph(
            url = url,
            username = username,
            password = password
        )
        pass
