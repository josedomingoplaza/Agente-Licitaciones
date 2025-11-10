from pymilvus import Collection, utility
from .connection import milvus_connection
from .schemas import licitation_schema   


class MilvusClient:
    def __init__(self):
        pass

    def create_licitation_collection(self, collection_name: str = "licitations") -> Collection:
        if not utility.has_collection(collection_name):
            print(f"Creating collection: {collection_name}")
            collection = Collection(name=collection_name, schema=licitation_schema)
            try:
                collection.create_partition("won_projects")
            except Exception:
                pass
            try:
                collection.create_partition("new_opportunities")
            except Exception:
                pass

            index_params = {
                "index_type": "IVF_FLAT",
                "metric_type": "L2",
                "params": {"nlist": 128}
            }
            try:
                collection.create_index(field_name="embedding", index_params=index_params)
            except Exception:
                pass

            collection.load()
            return collection

        print(f"Collection '{collection_name}' already exists.")
        collection = Collection(name=collection_name)
        return collection

    def insert_chunks(self, collection_name: str, chunks_data: list, partition_name: str | None = None):
        collection = Collection(name=collection_name)
        embeddings = []
        texts = []
        categories = []
        headings = []
        lic_ids = []
        doc_names = []

        for c in chunks_data:
            embeddings.append(c.get("embedding"))
            texts.append(c.get("text_content"))
            categories.append(c.get("category"))
            headings.append(c.get("original_heading"))
            lic_ids.append(c.get("licitation_id"))
            doc_names.append(c.get("document_name"))

        entities = [embeddings, texts, categories, headings, lic_ids, doc_names]
        if partition_name:
            result = collection.insert(entities, partition_name=partition_name)
        else:
            result = collection.insert(entities)

        collection.flush()
        return result

    def search(self, collection_name: str, query_vector: list, limit: int = 5, filter_expression: str | None = None, partition_names: list | None = None):
        collection = Collection(name=collection_name)
        collection.load()

        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}

        results = collection.search(
            data=[query_vector],
            anns_field="embedding",
            param=search_params,
            limit=limit,
            expr=filter_expression,
            partition_names=partition_names,
            output_fields=["text_content", "category", "licitation_id", "document_name"]
        )
        return results

