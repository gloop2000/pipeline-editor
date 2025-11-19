import subprocess
import sys
import os

# --- Configuration: replace these with your MongoDB details ---
mongo_uri = "mongodb://localhost:27017"  # Your Mongo URI
database = "test_db"                      # Database name
collection = "test_collection"            # Collection name
query = '{}'                              # Query as JSON string
output_csv = "output/test_data.csv"       # Output CSV file path

# Ensure output directory exists
os.makedirs(os.path.dirname(output_csv), exist_ok=True)

venv_python = sys.executable  # This points to the currently active Python in venv

# --- Run the YAML component logic via Python subprocess ---
command = [
    venv_python,
    "-c",
    f"""
import json
import pandas as pd
from pymongo import MongoClient
from pathlib import Path

mongo_uri = '{mongo_uri}'
database = '{database}'
collection = '{collection}'
query = '{query}'
output_path = '{output_csv}'
try:
    client = MongoClient(mongo_uri)
    db = client[database]
    col = db[collection]

    try:
        query_obj = json.loads(query)
    except Exception:
        print("Invalid JSON query. Using empty filter {{}} instead.")
        query_obj = {{}}

    data = list(col.find(query_obj))
    if not data:
        print("No data found for given query.")
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame().to_csv(output_path, index=False)
    else:
        df = pd.DataFrame(data)
        if "_id" in df.columns:
            df = df.drop(columns=["_id"])
        df.to_csv(output_path, index=False)
        print(f"Exported {{len(df)}} records to {{output_path}}")
        print(df.head())
finally:
    client.close()
"""
]

# Execute the command
subprocess.run(command, check=True)
print(f"CSV file should be available at: {output_csv}")
