from flask import request
from flask_restful import Resource
from pymongo import MongoClient
import requests
import json

from models.book import BookModel

class Book(Resource):
    def get(self):
        posted_data = request.get_json()

        if BookModel.book_exist() is None:
            return {"message":"no such book", "status code":200}

        return {"book":return_data, "message":"succesful", "status code":200}

    def post(self):
        posted_data = request.get_json()

        #Checking book is valid (only book name and book author can uniquely identify a book)
        if BookModel.validate_book() is not None:
            return BookModel.validate_book()

        #Checking if book already exists
        if BookModel.book_exist() is not None:
            return BookModel.book_exist()

        books.insert(posted_data)

        return {"message":"added book", "status code":200}

class SearchBook(Resource):
    def get(self):
        posted_data = request.get_json()

        #Querying data from database using a regular expression (regex)
        return_data = list(books.find({ "$or" : [ {'name':{"$regex":posted_data["search"]}} , {'author':{"$regex":posted_data["search"]}} ] }, {"_id":0} ))

        if len(return_data) == 0:
            return {"message":"no books found", "status code":200}

        #Returning a list of only book names and authors
        book_list = [{"name":book_index["name"], "author":book_index["author"]} for book_index in return_data]

        return {"books":book_list, "message":"succesful", "status code":200}

class Search_Google_Books(Resource):
    def get(self):
        posted_data = request.get_json()

        search_query = posted_data["search"]

        url=f"https://www.googleapis.com/books/v1/volumes?q={search_query}&key={security.api_key}"

        book_item_to_dict = lambda book : {"Title" : book["volumeInfo"]['title'], "Authors" : book["volumeInfo"]['authors'], "Description" : book["volumeInfo"].get('description', None), "Rating": book["volumeInfo"].get("averageRating", None)}

        request = json.loads(requests.get(url).text)
        book_items = request["items"]

        book_list = [book_item_to_dict(book) for book in book_items]

        if (len(book_list) = 0):
            return {"message":"no books found", "status code":404}

        return {"books":book_list, "message":"succesful", "status code":200}
