from flask import Flask
from flask_restful import Api

import resources.user as user
import resources.book as book
import resources.booklist as booklist
import resources.amazonapi as amazonapi

app = Flask(__name__)
api = Api(app)

api.add_resource(user.RegisterUser, "/registeruser")
api.add_resource(book.Book, "/book")
api.add_resource(book.SearchBook, "/search")
api.add_resource(booklist.BookList, "/booklist")
api.add_resource(book.Search_Google_Books), "/googlebooks"

if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
