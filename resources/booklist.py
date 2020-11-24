from flask import request
from flask_restful import Resource

from database.mongodb import book_lists
from models.booklist import BookListModel
import security

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
        # posted_data = request.get_json()
        #
        # booklist = book_lists.find_one({'name':posted_data["name"]}, {"_id":0} )["booklist"].insert

        return {"message":"book added succesfuly", "status code": 200}

class SearchList(Resource):
    #regex
    pass
