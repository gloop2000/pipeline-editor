import subprocess
import sys
import os

# --- Configuration: replace these with your InfluxDB details ---
url = "http://localhost:8181"  # InfluxDB server host
token = "apiv3_36lCnbmj5Py5xS7gOmCGkSMBWschAET-qFVPCXYyjz-WX7DQGhqWzbrQmcEtaio59mi73MYo_2Qs_xuVNIcpTQ"  # InfluxDB token
database = "test_db"  # Database name
query = "SELECT * FROM home"  # SQL query
output_csv = "output/influx_data.csv"  # Output CSV file path

# Ensure output directory exists
os.makedirs(os.path.dirname(output_csv), exist_ok=True)

venv_python = sys.executable  # Currently active Python in venv

# --- Run the YAML component logic via Python subprocess ---
command = [
    venv_python,
    "-c",
    f"""
import pandas as pd
from influxdb_client_3 import InfluxDBClient3
from pathlib import Path

url = '{url}'
token = '{token}'
database = '{database}'
query = '''{query}'''
output_path = '{output_csv}'

# Create client and query data
client = InfluxDBClient3(host=url, token=token, database=database)

try:
    result = client.query(query=query)
    # Convert PyArrow Table to pandas DataFrame
    if result is not None:
        df = result.to_pandas()
    else:
        df = pd.DataFrame()
    if df is None or df.empty:
        print("No data returned for the query.")
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame().to_csv(output_path, index=False)
    else:
        df.to_csv(output_path, index=False)
        print(f"Exported {{len(df)}} rows to {{output_path}}")
except Exception as e:
    print("Error querying InfluxDB:", e)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame().to_csv(output_path, index=False)
finally:
    client.close()
"""
]

# Execute the command
subprocess.run(command, check=True)
print(f"CSV file should be available at: {output_csv}")