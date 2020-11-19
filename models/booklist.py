from pymongo import MongoClient

import security

client = MongoClient(security.password)
db = client.objects

book_lists = db["book lists"]
books = db["books"]

class BookListModel:
    def create_list(posted_data):
        #Checking list is valid (name uniqely identifies list)
        if 'name' not in posted_data or (len(posted_data["name"]) == 0):
            return {"message": "list must contain name", "status code":422}

        name = posted_data["name"]
        booklist = posted_data.get("books", None)
        added_books = []

        if booklist is not None:
            for book in booklist:
                add_book = books.find_one({ "$and" : [ {'name':book["name"]} , {'author':book["author"]} ] }, {"_id":0} )
                if (add_book == None):
                    return {"message":"book doesn't exist", "status code": 404}
                added_books.append(add_book)

        book_lists.insert({"name":name, "books":added_books})

        return {"message":"book list added succesfuly", "status code": 200}

    def get_list(posted_data):
        pass

    def add_book_to_list(book, list):
        pass
