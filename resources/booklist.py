from flask import request
from flask_restful import Resource

from models.booklist import BookListModel

class BookList(Resource):
    def post(self):
        posted_data = request.get_json()

        #Checking list is valid (name uniqely identifies list)
        if 'name' not in posted_data or (len(posted_data["name"]) == 0):
            return {"message": "list must contain name", "status code":422}

        if book_lists.count_documents({'name':posted_data["name"]}, limit = 1) != 0 :
                return {"message":"booklist already exists", "status code":403}

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

    def get(self):
        pass

class AddToList(Resource):
    def post(self):
        pass
