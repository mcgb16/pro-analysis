from pymongo import MongoClient
import extras.info as ext

client = MongoClient(ext.string_connection)

conn = client[ext.db]

top5_collection = conn[ext.top5_collection]

def create_top5(top5_list):
    try:
        top5_insert = top5_collection.insert_many(top5_list)
        return top5_insert
    except Exception as e:
        print(e)
        return e