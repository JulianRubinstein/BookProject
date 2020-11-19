from flask import request
from flask_restful import Resource

from models.user import UserModel

class RegisterUser(Resource):
    def post(self):
        posted_data = request.get_json()
        insert_user = UserModel.insert(posted_data)
        return inser_tuser

class LogIn(Resource):
    def post(self):
        pass
