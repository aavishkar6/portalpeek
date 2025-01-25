from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

import os
from hashlib import sha256

from ..config import Config
from ..schemas.schemas import Announcements 

# Saving to database.
def save_announcements_to_database(announcements):

    db = get_db()
    collection = db.announcements

    for announcement in announcements:
        announcement["identifier"] = sha256(f"{announcement['date']}{announcement['title']}".encode()).hexdigest()

        inserted_id = insert_one(collection, announcement)

        print(f"Document inserted with _id: {inserted_id}")


    print("Successfully inserted announcements to the database.")


def get_db(db_name ='portalpeek'):
    try:
        # Create a new client and connect to the server
        client = MongoClient(os.getenv("MONGO_URI"))
        # Return the client
        return client[db_name]
    except Exception as e:
        print(e)

# CRUD Operations on MongoDB

def insert_one(collection, data: Announcements):
    """Insert one document into the collection."""
    try:
        result = collection.insert_one(data)
        if result.acknowledged:
            return result.inserted_id
        else:
            return ValueError
    except DuplicateKeyError:
        print(f"Duplicate announcement skipped: ")


def find_one(collection, query: str):
    """Find a document based on a query."""
    document = collection.find_one(query)
    if document:
        return document
    else:
        print("No document matches the query.")
        return ValueError
    
def delete_one(collection, query: str):
    """Delete a document based on a query"""
    document = collection.deleteOne(query)
    if document.acknowledged:
        print("Document successfully deleted")
    else:
        return ValueError





if __name__ == "__main__":
    db = get_db()
    collection = db['announcements']
    print(collection)