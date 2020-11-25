from database.mongodb import book_lists

class BookListModel:
    def validate_list(posted_data):
        if 'name' not in posted_data or (len(posted_data["name"]) == 0):
            return {"message": "list must contain name", "status code":422}

        if book_lists.count_documents({'name':posted_data["name"]}, limit = 1) != 0 :
                return {"message":"booklist already exists", "status code":403}

    def create_dict(posted_data):
        booklist={
            "name" : posted_data["name"],
            "booklist" : posted_data.get("books", []),
            "description" : posted_data.get("description", None),
            "playlist_author" : posted_data.get("playlist_author", None)
            }
        return booklist
