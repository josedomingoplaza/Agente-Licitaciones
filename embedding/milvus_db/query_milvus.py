from embedding.cohere_embedder import CohereEmbedder
from embedding.milvus_db.connection import milvus_connection
from embedding.milvus_db.client import MilvusClient

COLLECTION = "licitations"

embedder = CohereEmbedder()
milvus_connection.connect()
client = MilvusClient()

# Semantic search loop
while True:
	print("\nSemantic search: Enter a query to find relevant chunks.")
	query_text = input("Enter your search query: ").strip()
	if query_text:
		query_vec = embedder.embed_text(query_text, dim=1024)
		results = client.search(COLLECTION, query_vec, limit=5)
		print("\nTop semantic search results:")
		for idx, hit in enumerate(results[0] if isinstance(results[0], list) else results):
			print(f"Result {idx+1}:")
			print(hit)
			print("---")
