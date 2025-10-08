from pymilvus import FieldSchema, CollectionSchema, DataType

licitation_fields = [
    FieldSchema(
        name="id",
        dtype=DataType.INT64,
        is_primary=True,
        auto_id=True,
        description="Primary key for the chunk"
    ),

    FieldSchema(
        name="embedding",
        dtype=DataType.FLOAT_VECTOR,
        dim=1024, 
        description="Vector embedding of the text chunk"
    ),

    FieldSchema(
        name="text_content",
        dtype=DataType.VARCHAR,
        max_length=4000,
        description="The original text content of the chunk"
    ),

    FieldSchema(
        name="category",
        dtype=DataType.VARCHAR,
        max_length=256,
        description="Standardized category (e.g., 'Technical Requirements')"
    ),

    FieldSchema(
        name="original_heading",
        dtype=DataType.VARCHAR,
        max_length=512,
        description="The original heading from the source document"
    ),

    FieldSchema(
        name="licitation_id",
        dtype=DataType.VARCHAR,
        max_length=256,
        description="Unique identifier for the parent licitación document"
    ),

    FieldSchema(
        name="document_name",
        dtype=DataType.VARCHAR,
        max_length=512,
        description="The source PDF filename"
    )
]

licitation_schema = CollectionSchema(
    fields=licitation_fields,
    description="Schema for storing and searching licitación document chunks",
    enable_dynamic_field=False 
)