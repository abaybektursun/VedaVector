from pymilvus import connections, db, Collection, CollectionSchema, FieldSchema, DataType, utility

DB_NAME = "ABAY_TEST"

conn = connections.connect(host="127.0.0.1", port=19530)

dbs = db.list_database()
if not DB_NAME in dbs:
    database = db.create_database(DB_NAME)

db.using_database(DB_NAME)


# Setup  Collection ----------------------------------------------
fields = [
    FieldSchema(name="pk", dtype=DataType.INT64, is_primary=True, auto_id=False),
    FieldSchema(name="random", dtype=DataType.DOUBLE),
    FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=8)
]
schema = CollectionSchema(fields, "hello_milvus is the simplest demo to introduce the APIs")
hello_milvus = Collection("hello_milvus", schema)


# Setup schema---------------------------
collection_name = "test_collection"
if not utility.has_collection(collection_name):
    collection = Collection(
        name=collection_name,
        schema=schema,
        using='default',
        shards_num=2
    )


# Insert data---------------------------
import random
entities = [
    [i for i in range(3000)],  # field pk
    [float(random.randrange(-20, -10)) for _ in range(3000)],  # field random
    [[random.random() for _ in range(8)] for _ in range(3000)],  # field embeddings
]
insert_result = hello_milvus.insert(entities)
# After final entity is inserted, it is best to call flush to have no growing segments left in memory
hello_milvus.flush()  

index = {
    "index_type": "IVF_FLAT",
    "metric_type": "L2",
    "params": {"nlist": 128},
}
hello_milvus.create_index("embeddings", index)

hello_milvus.load()
vectors_to_search = entities[-1][-2:]
search_params = {
    "metric_type": "L2",
    "params": {"nprobe": 10},
}
result = hello_milvus.search(vectors_to_search, "embeddings", search_params, limit=3, output_fields=["random"])

result = hello_milvus.query(expr="random > -14", output_fields=["random", "embeddings"])

print(result)

# Clean up---------------------------
connections.disconnect("default")