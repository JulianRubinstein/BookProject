from flask import request
from flask_restful import Resource
from pymongo import MongoClient

import security

client = MongoClient(security.password)
db = client.objects
books = db["books"]

class BookMethods:
    def getbook(postedData):
        returnData = books.find_one({ "$and" : [ {'name':postedData["name"]} , {'author':postedData["author"]} ] }, {"_id":0} )

        if returnData == None :
            return {"message":"no such book", "status code":200}

        return {"book":returnData, "message":"succesful", "status code":200}

    def addbook(postedData):
        #Checking book is valid (only book name and book author can uniquely identify a book)
        if 'name' not in postedData or 'author' not in postedData:
            return {"message": "book must contain name and author", "status code":422}
        if (len(postedData["name"]) == 0 or len(postedData["author"]) == 0) :
            return {"message": "book must contain name and author", "status code":422}

        #Checking if book already exists
        if books.count_documents({ "$and" : [ {'name':postedData["name"]} , {'author':postedData["author"]} ] }, limit = 1) != 0 :
            return {"message":"book already exists", "status code":403}

        #Adding book
        books.insert(postedData)

        return {"message":"added book", "status code":200}

    def searchbook(postedData):
            #Querying data from database
            returnData = list(books.find({ "$or" : [ {'name':{"$regex":postedData["search"]}} , {'author':{"$regex":postedData["search"]}} ] }, {"_id":0} ))

            #Checking if no results
            if len(returnData) == 0:
                return {"message":"no books found", "status code":200}

            booklist = [{"name":bookindex["name"], "author":bookindex["author"]} for i in returnData]

            return {"books":booklist, "message":"succesful", "status code":200}


class Book(Resource):
    def get(self):
        #Get data
        postedData = request.get_json()
        getbook = BookMethods.getbook(postedData)
        return getbook

    def post(self):
        #Get data
        postedData = request.get_json()
        addbook = BookMethods.addbook(postedData)
        return addbook

class SearchBook(Resource):
    def get(self):
        #Get data
        posteData = request.get_json()
        searchbook = BookMethods.searchbook(postedData)
        return searchbook
