import os


class Config:

    
    URI = "bolt://localhost:7687"
    AUTH = ("neo4j", "my_pass")
    NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
    NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'missingu')
    HUGGINGFACE_MODEL = os.getenv('HUGGINGFACE_MODEL', 'google/flan-t5-large')
    #OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your-openai-key')