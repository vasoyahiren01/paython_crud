from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId
from config import config
import logging


class Database:
    def __init__(self):
        try:
            self.client = MongoClient(config['db']['url'])  # configure db url
            self.db = self.client[config['db']['name']]  # configure db name
        except Exception as e:
            logging.error(f"Database connection error: {e}")
            raise

    def insert(self, element, collection_name):
        element["createdAt"] = datetime.now()
        element["updatedAt"] = datetime.now()
        try:
            inserted = self.db[collection_name].insert_one(element)  # insert data to db
            return str(inserted.inserted_id)
        except Exception as e:
            logging.error(f"Insert error: {e}")
            return None

    def find(self, criteria, collection_name, projection=None, sort=None, limit=0, cursor=False):  # find all from db
        if "_id" in criteria:
            criteria["_id"] = ObjectId(criteria["_id"])

        try:
            found = self.db[collection_name].find(filter=criteria, projection=projection, limit=limit, sort=sort)
            if cursor:
                return found
            return [self._serialize_id(doc) for doc in found]
        except Exception as e:
            logging.error(f"Find error: {e}")
            return []

    def find_one(self, criteria, collection_name, projection=None):  # find One from db
        try:
            found = self.db[collection_name].find_one(filter=criteria, projection=projection)
            return self._serialize_id(found) if found else None
        except Exception as e:
            logging.error(f"Find one error: {e}")
            return None

    def find_by_id(self, id, collection_name):
        return self.find_one({"_id": ObjectId(id)}, collection_name)

    def update(self, id, element, collection_name):
        criteria = {"_id": ObjectId(id)}
        element["updatedAt"] = datetime.now()
        set_obj = {"$set": element}  # update value

        try:
            updated = self.db[collection_name].update_one(criteria, set_obj)
            return updated.matched_count == 1
        except Exception as e:
            logging.error(f"Update error: {e}")
            return False

    def delete(self, id, collection_name):
        try:
            deleted = self.db[collection_name].delete_one({"_id": ObjectId(id)})
            return deleted.deleted_count == 1
        except Exception as e:
            logging.error(f"Delete error: {e}")
            return False

    def _serialize_id(self, document):
        if document and "_id" in document:
            document["_id"] = str(document["_id"])
        return document
