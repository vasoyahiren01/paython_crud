from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime
from dotenv import load_dotenv
import os


class DatabaseManager:
    def __init__(self):
        self.db_client = {}
        self.db_list = {}
        self.model_list = {}

    def connect(self):
        """
        Initialize connections to multiple databases
        """
        try:

            # Load environment variables from a .env file
            load_dotenv()

            env = os.environ
            db1_params = {
                "driver": env.get("DB1_DRIVER"),
                "host": env.get("DB1_HOST"),
                "port": env.get("DB1_PORT"),
                "user": env.get("DB1_USER"),
                "password": env.get("DB1_PASS"),
                "name": env.get("DB1_NAME"),
                "identifier": env.get("DB1_IDENTIFIER"),
            }
            print("DB connected ", db1_params)


            db2_params = {
                "driver": env.get("DB2_DRIVER"),
                "host": env.get("DB2_HOST"),
                "port": env.get("DB2_PORT"),
                "user": env.get("DB2_USER"),
                "password": env.get("DB2_PASS"),
                "name": env.get("DB2_NAME"),
                "identifier": env.get("DB2_IDENTIFIER"),
            }

            # Initialize client connections
            self.init_client_db_connection(**db1_params)
            # Uncomment the next line to add the second database connection
            # self.init_client_db_connection(**db2_params)

            # Example to load the default database
            self.master_db = self.get_db("DB1", "ubs")
            print("DB connected successfully")
        except Exception as e:
            print(f"DB Connection error: {e}")

    def get_db(self, db_identifier, db_name):
        """
        Get or create a database connection for the given identifier and name.
        """
        key = f"{db_identifier}_{db_name}"
        if key in self.db_list:
            return self.db_list[key]
        else:
            db_client = self.db_client.get(db_identifier)
            if db_client:
                db = db_client[db_name]
                self.db_list[key] = db
                return db
            else:
                raise ValueError(f"No client found for identifier: {db_identifier}")

    def get_model(self, db, schema, schema_definitions):
        """
        Get or create a model for the given database and schema.
        """
        key = f"{db.name}_{schema}"
        if key in self.model_list:
            return self.model_list[key]
        else:
            model_obj = db[schema]
            self.model_list[key] = model_obj
            return model_obj

    def init_client_db_connection(self, driver, host, port, user, password, name, identifier):
        """
        Initialize a MongoDB client connection.
        """
        try:
            connection_string = f"{driver}://"
            if user and password:
                connection_string += f"{user}:{password}@"
            connection_string += f"{host}:{port}/{name}"

            client = MongoClient(connection_string, maxPoolSize=100, serverSelectionTimeoutMS=5000)
            # Test connection
            client.admin.command("ping")
            print(f"MongoDB connected to {connection_string}")

            self.db_client[identifier] = client
        except ConnectionFailure as e:
            print(f"MongoDB Connection Error>> : {e}")
            raise

    def close_all_connections(self):
        """
        Close all database connections.
        """
        for identifier, client in self.db_client.items():
            client.close()
            print(f"Closed connection for {identifier}")


# Example usage
if __name__ == "__main__":
    db_manager = DatabaseManager()
    db_manager.connect()

    # Example usage of getting a database or model
    try:
        db = db_manager.get_db("DB1", "ubs")
        print("Successfully loaded the database")
    except Exception as e:
        print(f"Error loading database: {e}")
