from pymongo import MongoClient
import extras.info as ext

client = MongoClient(ext.string_connection)

db_conn = client[ext.db]