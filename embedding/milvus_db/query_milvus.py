from embedding.cohere_embedder import CohereEmbedder
from embedding.milvus_db.connection import milvus_connection
from embedding.milvus_db.client import MilvusClient

COLLECTION = "licitations"

embedder = CohereEmbedder()
milvus_connection.connect()
client = MilvusClient()

filter_value = "Información Administrativa y General"
filter_expression = f'category == "{filter_value}"'

while True:
    print("\nSemantic search: Enter a query to find relevant chunks.")
    query_text = input("Enter your search query: ").strip()
    if query_text:
        query_vec = embedder.embed_text(query_text, dim=1024)
        results = client.search(
            collection_name=COLLECTION,
            query_vector=query_vec, 
            limit=5,
            filter_expression=filter_expression, 
        )
        print("\nTop semantic search results:")
        for idx, hits in enumerate(results):
            print(f"TopK results for query {idx+1}:")
            for hit in hits:
                print(hit)
                print("---")