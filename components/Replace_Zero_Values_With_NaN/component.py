import subprocess
import sys
import os

# --- Configuration: replace these with your MongoDB details ---
input_csv = "test_data.csv"       # Input CSV file path
columns = '["Glucose", "BloodPressure", "BMI","Insulin"]'  # Columns to process as JSON array string
output_csv = "output/clean_test_data.csv"       # Output CSV file path

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
import numpy as np
from pathlib import Path
import os

input_csv = '{input_csv}'
output_path = '{output_csv}'
columns = '{columns}'

df = pd.read_csv(input_csv)
try:
    cols = json.loads(columns)
    if not isinstance(cols, list):
        raise ValueError
except Exception:
    raise ValueError("Columns parameter must be a valid JSON array of column names.")

for col in cols:
    if col in df.columns:
        df[col] = df[col].replace(0, np.nan)
    else:
        print(f"Warning: Column '{{col}}' not found in dataset.")

df.to_csv(output_path, index=False)
print(f"Processed CSV saved to {{output_path}}")
"""
]

# Execute the command
subprocess.run(command, check=True)
print(f"CSV file should be available at: {output_csv}")
