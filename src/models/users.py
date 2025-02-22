from helper.validation import Validator
from helper.database import Database

class Users:
    def __init__(self):
        self.validator = Validator()
        self.db = Database()
        self.collection_name = 'users'

        self.fields = {
            "name": "string",
            "email": "string",
            "mobile": "int",
            "password": "string",
            "dob": "datetime",
            "profile": "string",
            "createdAt": "datetime",
            "updatedAt": "datetime",
        }

        self.create_required_fields = ["name", "mobile", "email", "password"]
        self.update_required_fields = ["name", "mobile"]

    def create(self, user_data):
        self.validator.validate(user_data, self.fields, self.create_required_fields)
        res = self.db.insert(user_data, self.collection_name)
        return {"message": "User created", "id": res}

    def find(self, query, projection=None):
        return self.db.find(query, self.collection_name, projection)

    def find_one(self, query):
        return self.db.find_one(query, self.collection_name)

    def find_by_id(self, user_id):
        return self.db.find_by_id(user_id, self.collection_name)

    def update(self, user_id, user_data):
        self.validator.validate(user_data, self.fields, self.update_required_fields)
        return self.db.update(user_id, user_data, self.collection_name)

    def delete(self, user_id):
        return self.db.delete(user_id, self.collection_name)
