from flask import request
from flask_restful import Resource
from pymongo import MongoClient

import security

client = MongoClient(security.password)
db = client.objects
bookLists = db["book lists"]

class BookList(Resource):
    def post(self):
        pass

    def get(self):
        pass
