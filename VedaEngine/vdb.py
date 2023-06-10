from pymilvus import connections, db, Collection, CollectionSchema, FieldSchema, DataType, utility

DB_NAME = "ABAY_TEST"

conn = connections.connect(host="127.0.0.1", port=19530)

dbs = db.list_database()
if not DB_NAME in dbs:
    database = db.create_database(DB_NAME)

db.using_database(DB_NAME)


# Setup  Collection ----------------------------------------------
doc_id = FieldSchema(
  name="doc_id",
  dtype=DataType.INT64,
  is_primary=True,
)
doc_name = FieldSchema(
  name="doc_name",
  dtype=DataType.VARCHAR,
  max_length=200,
)
word_count = FieldSchema(
  name="word_count",
  dtype=DataType.INT64,
)
doc_intro = FieldSchema(
  name="doc_intro",
  dtype=DataType.FLOAT_VECTOR,
  dim=2
)
schema = CollectionSchema(
  fields=[doc_id, doc_name, word_count, doc_intro],
  description="Test doc search",
  enable_dynamic_field=True
)


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
data = [
  [i for i in range(2000)],
  [str(i) for i in range(2000)],
  [i for i in range(10000, 12000)],
  [[random.random() for _ in range(2)] for _ in range(2000)]
]

data.append([str("dy"*i) for i in range(2000)])

collection = Collection(collection_name)      # Get an existing collection.
mr = collection.insert(data)



# Clean up---------------------------
connections.disconnect("default")