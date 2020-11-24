from bcrypt import hashpw, gensalt

from database.mongodb import users

class UserModel:
    def registrate(posted_data):
        if 'username' not in posted_data or 'password' not in posted_data or 'email' not in posted_data:
            return {"message": "please enter username, password and email", "status code":422}

        username, password = posted_data["username"], posted_data["password"]
        email = posted_data.get("email", None)

        if (len(password) <= 5):
            return {"message":"password too short", "status code":401}

        if (len(username) <= 4):
            return {"message":"username too short", "status code":401}

        if "@" not in email or "." not in email:
            return {"message":"please enter valid email", "status code":401}

        if users.count_documents({'username': username}, limit = 1) != 0 :
            return {"message":"username already exists", "status code":403}

        if users.count_documents({'email': email}, limit = 1) != 0 :
            return {"message":"email already exists", "status code":403}

    def authenticate(posted_data):
        username, password = posted_data["username"], posted_data["password"]

        if users.count_documents({'username': username}, limit = 1) == 0 :
            return {"message":"wrong username or password", "status code":401}

        hashed_password = users.find_one({"username":username})["password"]

        if hashpw(password.encode('utf8'), hashed_password) != hashed_password:
                return {"message":"wrong username or password", "status code":401}
