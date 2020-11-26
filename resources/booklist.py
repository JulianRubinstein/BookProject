from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from database.mongodb import book_lists
from models.booklist import BookListModel
from models.book import BookModel

class BookList(Resource):
    @jwt_required
    def post(self):
        posted_data = request.get_json()
        posted_data["playlist_author"] = get_jwt_identity()["username"]

        if get_jwt_identity()["access level"] <= 1:
            return {"message":"only admins", "user":get_jwt_identity() ,"status code": 401}

        if BookListModel.validate_list(**posted_data):
            return BookListModel.validate_list(**posted_data)

        booklist_instance = BookListModel(**posted_data)

        book_lists.insert(booklist_instance.to_dict())

        return {"message":"book list added succesfuly", "user":get_jwt_identity() ,"status code": 200}

    @jwt_required
    def get(self):
        posted_data = request.get_json()

        booklist = book_lists.find_one({'name':posted_data["name"]}, {"_id":0} )

        if booklist == None:
                return {"message":"book list not found", "status code": 404}

        return {"book list":booklist, "user":get_jwt_identity(), "message":"succesful", "status code": 200}

class AddToList(Resource):
    @jwt_required
    def post(self):
        posted_data = request.get_json()

        if get_jwt_identity()["access level"] <= 1:
            return {"message":"only admins", "user":get_jwt_identity() ,"status code": 401}

        if BookModel.validate_book(**posted_data["book"]):
            return BookModel.validate_book(**posted_data["book"])

        if book_lists.count_documents({'name':posted_data["booklist name"]}, limit = 1) == 0 :
                return {"message":"booklist doesn't exist", "status code":404}

        book_lists.update({"name": posted_data["booklist name"]},{"$push": {'booklist': posted_data["book"]}})

        return {"message":"book added succesfuly", "user":get_jwt_identity(), "status code": 200}

class SearchList(Resource):
    @jwt_required
    def get(self):
        posted_data = request.get_json()

        return_data = list(book_lists.find({ "$or" : [ {'name':{"$regex":posted_data["search"]}} , {'playlist_author':{"$regex":posted_data["search"]}} ] }, {"_id":0} ))

        if len(return_data) == 0:
            return {"message":"no booklists found", "status code":404}

        return {"book lists": return_data, "user":get_jwt_identity(), "message":"succesful", "status code":200}
