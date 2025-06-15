from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

import os
from hashlib import sha256
from typing import Optional, Union

from ..config import Config
from ..schemas.schemas import Announcements 

# Saving to database.
def save_announcements_to_database(announcements: list[dict]) -> None:

    db = get_db()
    collection = db.announcements

    for announcement in announcements:
        announcement["identifier"] = sha256(f"{announcement['date']}{announcement['title']}".encode()).hexdigest()

        insert_one(collection, announcement)

    print("Successfully inserted announcements to the database.")


def get_db(db_name :str ='portalpeek') -> MongoClient:
    try:
        # Create a new client and connect to the server
        client = MongoClient(os.getenv("MONGO_URI"))
        # Return the client
        return client[db_name]
    except Exception as e:
        print(e)

# CRUD Operations on MongoDB

def insert_one(collection_db , data: dict) -> None:
    """Insert one document into the collection."""
    try:
        result = collection_db.insert_one(data)
        if result.acknowledged:
            print(f"Document inserted with _id: {result.inserted_id}")
    except DuplicateKeyError:
        print(f"Duplicate announcement skipped: ")
        return None
    except Exception as e:
        print(f"Error occured : {e}")
        return None

def get_all(collection):
    """Returns all the db documents from the collection."""

    return collection.find({})

def find_one(collection, query: dict) -> Optional[dict]:
    """Find a document based on a query."""
    document = collection.find_one(query)
    if document:
        return document
    else:
        print("No document matches the query.")
        return ValueError
    
def find_documents(collection, query: dict) -> Optional[dict]:
    """Return documents that match a given query"""
    documents = list(collection.find(query))
    if documents:
        return documents
    else:
        print("No document match the given query")
        return ValueError

def delete_one(collection, query: dict) :
    """Delete a document based on a query"""
    document = collection.deleteOne(query)
    if document.acknowledged:
        print("Document successfully deleted")
    else:
        return ValueError

def get_identifiers(collection):
    """Returns identifiers for all the documents stored in the db."""
    documents = get_all(collection)

    print(documents[0])

    identifiers = [each['identifier'] for each in documents]

    print(identifiers)

    return identifiers




if __name__ == "__main__":
    db = get_db()
    collection = db['announcements']
    print(collection)