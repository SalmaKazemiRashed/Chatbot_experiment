from neo4j import GraphDatabase
from .config import Config

class Neo4jClient:
    def __init__(self):
        self.driver = GraphDatabase.driver(Config.NEO4J_URI, auth=(Config.NEO4J_USER, Config.NEO4J_PASSWORD))  # this is for connection test

    def get_relevant_context(self, query):
        with self.driver.session() as session:
            cypher_query = (
                "MATCH (p:Protein)-[:RELATED_TO*1..2]-(related) "
                "WHERE toLower(p.name) CONTAINS toLower($query) "
                "RETURN p.name AS protein, collect(related.name) AS related_entities LIMIT 5"
            )
            result = session.run(cypher_query, query=query)
            context = []
            for record in result:
                context.append(f"Protein: {record['protein']}, Related: {record['related_entities']}")
            return "\n".join(context) if context else "No relevant context found."