from elasticsearch import Elasticsearch

es = Elasticsearch(
    "http://localhost:9201",
    headers={"X-Elastic-Product": "Elasticsearch"}
)

INDEX_NAME = "properties"

def create_index():
    if es.indices.exists(index=INDEX_NAME):
        print(f"Index '{INDEX_NAME}' already exists.")
        return

    mappings = {
        "mappings": {
            "properties": {
                "property_id": {"type": "keyword"},
                "description": {"type": "text"},
                "status": {"type": "keyword"},
                "neighborhood": {"type": "text"},
                "description_embedding": {
                    "type": "dense_vector",
                    "dims": 1536  # OpenAI embedding size
                }
            }
        }
    }

    es.indices.create(index=INDEX_NAME, body=mappings)
    print(f"Index '{INDEX_NAME}' created.")

if __name__ == "__main__":
    create_index()
