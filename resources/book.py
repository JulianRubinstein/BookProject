from flask import request
from flask_restful import Resource

from models.book import BookModel

class Book(Resource):
    def get(self):
        posted_data = request.get_json()
        getbook = BookModel.getbook(posted_data)
        return getbook

    def post(self):
        posted_data = request.get_json()
        addbook = BookModel.addbook(posted_data)
        return addbook

class SearchBook(Resource):
    def get(self):
        posted_data = request.get_json()
        searchbook = BookModel.searchbook(posted_data)
        return searchbook
