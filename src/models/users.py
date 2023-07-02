from helper.validation import Validator
from helper.database import Database
class Users(object):
    def __init__(self):
        self.validator = Validator()
        self.db = Database()

        self.collection_name = 'users'  # collection name

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

        # Fields optional for CREATE
        self.create_optional_fields = []

        # Fields required for UPDATE
        self.update_required_fields = ["name", "mobile"]

        # Fields optional for UPDATE
        self.update_optional_fields = []

    def create(self, users):
        # Validator will throw error if invalid
        self.validator.validate(users, self.fields, self.create_required_fields, self.create_optional_fields)
        res = self.db.insert(users, self.collection_name)
        return "Inserted Id " + res

    def find(self, users):  # find all
        return self.db.find(users, self.collection_name)

    def find_one(self, query):  # find One
        return self.db.find_one(query, self.collection_name)

    def find_by_id(self, id):
        return self.db.find_by_id(id, self.collection_name)

    def update(self, id, users):
        self.validator.validate(users, self.fields, self.update_required_fields, self.update_optional_fields)
        return self.db.update(id, users,self.collection_name)

    def updateOne(self, id, users):
        return self.db.update(id, users,self.collection_name)

    def delete(self, id):
        return self.db.delete(id, self.collection_name)
