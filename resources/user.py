from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
import datetime

from models.user import UserModel
from database.mongodb import users
import security

class RegisterUser(Resource):
    def post(self):
        posted_data = request.get_json()

        if UserModel.registrate(posted_data) is not None:
            return UserModel.registrate(posted_data)

        hashed_password = hashpw(posted_data["password"].encode('utf8'), gensalt())
        posted_data["password"] = hashed_password

        users.insert(posted_data)

        return {"message":"user signed succesfuly", "status code":201}

class LogIn(Resource):
    def get(self):
        posted_data = request.get_json()

        if UserModel.authenticate(posted_data) is not None:
            return UserModel.authenticate(posted_data)

        access_token = create_access_token(identity={"username":posted_data["username"]}, expires_delta= datetime.timedelta(minutes=60))

        return ({"access token":access_token, "message":"succesful", "status code":200})
