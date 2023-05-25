import openai
from pymilvus import CollectionSchema, FieldSchema, DataType, Collection


def create_db(collection_name="book"):
    # Prepare Schema
    book_id = FieldSchema(
        name="book_id", dtype=DataType.INT64, is_primary=True)
    book_intro = FieldSchema(
        name="book_intro", dtype=DataType.FLOAT_VECTOR, dim=2)
    schema = CollectionSchema(
        fields=[book_id, book_intro], description="Test book search")
    # Create a collection with the schema
    collection = Collection(name=collection_name,
                            schema=schema, using='default', shards_num=2)


def create_vector(x=""):
    v = openai.Embedding.create(input=x, engine='text-embedding-ada-002')
    v_res = v['data'][0]['embedding']
    print(len(v_res))
    return v_res


def insert_vector(v=""):
    collection = Collection("book")
    collection.insert(collection_name="book", records=v)


def search_vector():
    collection = Collection("book")
    search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
    results = collection.search(
        data=[[0.1, 0.2]],
        anns_field="book_intro",
        param=search_params,
        limit=10,
        expr=None
    )
    print(results)


def main():
    create_db()
    x = "我今天 sd很忙的我s ad今天很忙的我今 sd sd 天sd 很忙的我今天很dsa 忙的ds 我今天很忙sda 的我今天很忙的我今天很忙的"
    v = create_vector(x)
    insert_vector(v)
    search_vector()


main()