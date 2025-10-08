# milvus_db/client.py

from pymilvus import Collection, utility
from .connection import milvus_connection # Import our connection manager
from .schemas import licitation_schema   # Import the schema you defined

class MilvusClient:
    def __init__(self):
        milvus_connection.connect() # Ensure we are connected

    def create_licitation_collection(self):
        collection_name = "licitations"
        if not utility.has_collection(collection_name):
            print(f"Creating collection: {collection_name}")
            collection = Collection(name=collection_name, schema=licitation_schema)
            # Create partitions, indexes, etc. here
            collection.create_partition("won_projects")
            collection.create_partition("new_opportunities")
            # ... create index ...
            return collection
        else:
            print(f"Collection '{collection_name}' already exists.")
            return Collection(name=collection_name)

    def insert_chunks(self, collection_name: str, chunks_data: list, partition_name: str):
        collection = Collection(name=collection_name)
        print(f"Inserting {len(chunks_data)} chunks into partition '{partition_name}'...")
        # ... logic to format data and insert into the collection ...
        # e.g., collection.insert(data=chunks_data, partition_name=partition_name)
        collection.flush()
        print("Insertion complete.")

    def search(self, collection_name: str, query_vector: list, filter_expr: str, partition_names: list):
        collection = Collection(name=collection_name)
        collection.load()
        # ... logic to perform the search ...
        # e.g., results = collection.search(...)
        pass

# You can create a single instance to be used by the rest of your app
milvus_client = MilvusClient()