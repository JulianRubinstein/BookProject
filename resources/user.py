from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from bcrypt import hashpw, gensalt
import datetime

from models.user import UserModel
from database.mongodb import users
import security

class RegisterUser(Resource):
    def post(self):
        posted_data = request.get_json()
        user_instance = UserModel(**posted_data)

        if UserModel.registrate(**user_instance.to_dict()):
            return UserModel.registrate(**user_instance.to_dict())

        hashed_password = hashpw(user_instance.password.encode('utf8'), gensalt())
        user_instance.password = hashed_password

        users.insert(user_instance.to_dict())

        return {"message":"user signed succesfuly", "status code":201}

class LogIn(Resource):
    def get(self):
        posted_data = request.get_json()
        access_level = users.find_one({"username":posted_data["username"]})["access"]

        if UserModel.authenticate(**posted_data):
            return UserModel.authenticate(**posted_data)

        access_token = create_access_token(identity={"username":posted_data["username"], "access level":access_level}, expires_delta= datetime.timedelta(minutes=60))

        return ({"access token":access_token, "message":"succesful", "status code":200})
