import pandas as pd
from openpyxl import Workbook
from pymongo import MongoClient

def fetch_data_in_chunks(db, collection, query={}, projection=None, chunk_size=100000):
    """
    Fetch data from MongoDB in chunks.
    
    :param db: The database instance.
    :param collection: The collection name.
    :param query: The query to filter data.
    :param projection: The fields to project.
    :param chunk_size: Number of records per chunk.
    :yield: A chunk of data as a list of dictionaries.
    """
    cursor = db[collection].find(query, projection)
    chunk = []
    for i, doc in enumerate(cursor):
        chunk.append(doc)
        if (i + 1) % chunk_size == 0:
            yield chunk
            chunk = []
    if chunk:  # Yield remaining data
        yield chunk

def process_and_export_from_db(db, collection, query={}, projection=None, excel_file="output.xlsx", chunk_size=100000):
    """
    Process data fetched from a database in chunks and export to an Excel file.
    
    :param db: The database instance.
    :param collection: The collection name.
    :param query: The query to filter data.
    :param projection: The fields to project.
    :param excel_file: The output Excel file name.
    :param chunk_size: Number of records per chunk.
    """
    # Check if the Excel file already exists
    file_exists = False
    with pd.ExcelWriter(excel_file, engine='openpyxl', mode='a' if file_exists else 'w') as writer:
        for chunk_index, chunk_data in enumerate(fetch_data_in_chunks(db, collection, query, projection, chunk_size)):
            print(f"Processing chunk {chunk_index + 1}...")

            # Convert the chunk to a DataFrame
            df = pd.DataFrame(chunk_data)

            # Flatten nested fields if necessary (e.g., `data` field)
            if 'data' in df.columns:
                data_field = pd.json_normalize(df['data'])
                df = pd.concat([df.drop('data', axis=1), data_field], axis=1)

            # Write the chunk to Excel
            df.to_excel(writer, index=False, header=not file_exists if chunk_index > 0 else True)
            file_exists = True  # Set to True after the first chunk

    print(f"Excel file saved as {excel_file}")

# Example Usage
if __name__ == "__main__":
    # MongoDB connection
    client = MongoClient("mongodb://localhost:27017")  # Replace with your MongoDB URI
    db = client["ubs"]  # Replace with your database name

    # Define the collection and query
    collection_name = "hrms_sync"  # Replace with your collection name
    query = {}  # Define your query (e.g., {"sync": True})
    projection = {
        "_id": 1,
        "sync": 1,
        "data": 1,
        "createdAt": 1
    }  # Define the fields to project

    # Process and export data from MongoDB to Excel
    process_and_export_from_db(
        db=db,
        collection=collection_name,
        query=query,
        projection=projection,
        excel_file="database_output.xlsx",
        chunk_size=100000
    )
