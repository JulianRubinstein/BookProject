from pymongo import MongoClient

import security

client = MongoClient(security.password)
db = client.objects
books = db["books"]

class BookModel:
    def validate_book(posted_data):
        if 'name' not in posted_data or 'author' not in posted_data:
            return {"message": "book must contain name and author", "status code":422}
        if (len(posted_data["name"]) == 0 or len(posted_data["author"]) == 0) :
            return {"message": "book must contain name and author", "status code":422}

    def book_exist(posted_data):
        if books.count_documents({ "$and" : [ {'name':posted_data["name"]} , {'author':posted_data["author"]} ] }, limit = 1) != 0 :
            return {"message":"book already exists", "status code":403}  
