from flask import request
from flask_restful import Resource

from models.booklist import BookListModel

class BookList(Resource):
    def post(self):
        posted_data = request.get_json()
        insert_booklist = BookListModel.create_list(posted_data)
        return insert_booklist

    def get(self):
        posted_data = request.get_json()
        get_booklist = BookListModel.get_list(posted_data)
        return get_booklist

class AddToList(Resource):
    def post(self):
        pass
