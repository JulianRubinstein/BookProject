from pymongo import MongoClient

import security

client = MongoClient(security.password)
db = client.objects

book_lists = db["book lists"]
books = db["books"]

class BookListModel:
    def create_list(posted_data):
        pass

    def get_list(posted_data):
        pass

    def add_book_to_list(book, list):
        pass
