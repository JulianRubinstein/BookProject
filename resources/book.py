from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
import requests
import json

from models.book import BookModel
import security

class SearchBooks(Resource):
    @jwt_required
    def get(self):
        posted_data = request.get_json()

        search_query = posted_data["search"]

        url=f"https://www.googleapis.com/books/v1/volumes?q={search_query}&key={security.api_key}"

        book_item_to_dict = lambda book : {"Title" : book["volumeInfo"]['title'], "Authors" : book["volumeInfo"].get('authors', None), "Description" : book["volumeInfo"].get('description', None), "Rating": book["volumeInfo"].get("averageRating", None)}

        req = json.loads(requests.get(url).text)
        book_items = req["items"]

        book_list = [book_item_to_dict(book) for book in book_items]

        if (len(book_list) == 0):
            return {"message":"no books found", "status code":404}

        return {"books":book_list, "user":get_jwt_identity(), "message":"succesful", "status code":200}
