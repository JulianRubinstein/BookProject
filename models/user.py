from bcrypt import hashpw, gensalt

from database.mongodb import users
import security

class UserModel:
    def registrate(username, password):
            if (len(password) <= 5):
                return {"message":"password too short", "status code":401}

            if (len(username) <= 4):
                return {"message":"username too short", "status code":401}

            if users.count_documents({'username': username}, limit = 1) != 0 :
                return {"message":"username already exists", "status code":403}

    def authenticate(username, password):
        if users.count_documents({'username': username}, limit = 1) == 0 :
            return {"message":"wrong username or password", "status code":401}

        hashedPassword = users.find_one({"username":username})["password"]

        if hashpw(password.encode('utf8'), hashedPassword) != hashedPassword:
                return {"message":"wrong username or password", "status code":401}
