from pymongo import MongoClient
import security

client = MongoClient(security.password)
db = client.objects

users = db["users"]
book_lists = db["book lists"]
