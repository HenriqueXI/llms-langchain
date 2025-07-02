from elasticsearch import Elasticsearch
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from llms.llm_keys import OPENAI_API_KEY

class Indexer:
    def __init__(self):
        self.es = Elasticsearch(
            "http://localhost:9201",
            headers={"X-Elastic-Product": "Elasticsearch"}
        )
        self.index_name = "properties"

        # Embeddings: HuggingFace por padrão
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # Se quiser OpenAI Embeddings:
        # self.embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

    def embed(self, text: str):
        return self.embeddings.embed_query(text)

    def index_properties(self):
        properties = [
            {
                "property_id": "prop_001",
                "description": "Apartamento amplo no bairro Centro com 3 quartos, 2 banheiros e 1 vaga de garagem.",
                "status": "available",
                "neighborhood": "Centro"
            },
            {
                "property_id": "prop_002",
                "description": "Casa com quintal no bairro Jardim América, 2 quartos, excelente localização.",
                "status": "unavailable",
                "neighborhood": "Jardim América"
            },
            {
                "property_id": "prop_003",
                "description": "Cobertura duplex no bairro Centro com vista panorâmica e área gourmet.",
                "status": "available",
                "neighborhood": "Centro"
            }
        ]

        for prop in properties:
            vector = self.embed(prop["description"])
            doc = {
                **prop,
                "description_embedding": vector
            }
            self.es.index(index=self.index_name, id=prop["property_id"], document=doc)
            print(f"Indexed {prop['property_id']}")

        return f"Indexed {len(properties)} properties successfully."
