from pymongo import MongoClient

import security

client = MongoClient(security.password)
db = client.objects
bookLists = db["book lists"]
books = db["books"]

class BookListModel:


    def create_list(name, books=[]):


    def add_book_to_list(book, list):
