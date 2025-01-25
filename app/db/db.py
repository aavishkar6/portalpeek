from pymongo import MongoClient
import os

from ..config import Config


def get_db(db_name ='portalpeek'):
    try:
        # Create a new client and connect to the server
        client = MongoClient(os.getenv("MONGO_URI"))
        # Return the client
        return client[db_name]
    except Exception as e:
        print(e)

# CRUD Operations on MongoDB





if __name__ == "__main__":
    db = get_db()
    collection = db['announcements']
    print(collection)