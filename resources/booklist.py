from flask import request
from flask_restful import Resource

from database.mongodb import book_lists
from models.booklist import BookListModel
from models.book import BookModel

class BookList(Resource):
    def post(self):
        posted_data = request.get_json()

        if BookListModel.validate_list(posted_data) is not None:
            return BookListModel.validate_list(posted_data)

        booklist = BookListModel.create_dict(posted_data)

        book_lists.insert(booklist)

        return {"message":"book list added succesfuly", "status code": 200}

    def get(self):
        posted_data = request.get_json()

        booklist = book_lists.find_one({'name':posted_data["name"]}, {"_id":0} )

        if booklist == None:
                return {"message":"book list not found", "status code": 404}

        return {"book list":booklist, "message":"succesful", "status code": 200}

class AddToList(Resource):
    def post(self):
        posted_data = request.get_json()

        BookModel.validate_book(posted_data["book"])

        if book_lists.count_documents({'name':posted_data["booklist name"]}, limit = 1) == 0 :
                return {"message":"booklist doesn't exist", "status code":404}

        book_lists.update({"name": posted_data["booklist name"]},{"$push": {'booklist': posted_data["book"]}})

        return {"message":"book added succesfuly", "status code": 200}

class SearchList(Resource):
    def get(self):
        posted_data = request.get_json()

        return_data = list(book_lists.find({ "$or" : [ {'name':{"$regex":posted_data["search"]}} , {'playlist_author':{"$regex":posted_data["search"]}} ] }, {"_id":0} ))

        if len(return_data) == 0:
            return {"message":"no booklists found", "status code":404}

        return {"book lists": return_data,"message":"succesful", "status code":200}
