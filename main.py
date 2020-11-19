from flask import Flask
from flask_restful import Api

import resources.user as user
import resources.book as book
import resources.booklist as booklist

app = Flask(__name__)
api = Api(app)

api.add_resource(user.RegisterUser, "/registeruser")
api.add_resource(book.Book, "/book")
api.add_resource(book.SearchBook, "/search")

if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
