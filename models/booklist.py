from database.mongodb import book_lists

class BookListModel:
    def __init__(self, name, playlist_author, books = [], description = "", **kwargs):
        self.name = name
        self.playlist_author = playlist_author
        self.books = books
        self.description = description

    def to_dict(self):
        booklist={
            "name" : self.name,
            "playlist_author" : self.playlist_author,
            "booklist" : self.books,
            "description" : self.description
            }
        return booklist

    def validate_list(name, **kwargs):
        if len(name) == 0:
            return {"message": "list must contain name", "status code":422}

        if book_lists.count_documents({'name':name}, limit = 1) != 0 :
                return {"message":"booklist already exists", "status code":403}
