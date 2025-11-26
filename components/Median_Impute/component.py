import subprocess
import sys
import os

# --- Configuration: replace these with your MongoDB details ---
input_csv = "test_data.csv"       # Input CSV file path
columns = '["Glucose", "BloodPressure", "BMI","Insulin","SkinThickness"]'  # Columns to process as JSON array string
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

# Parse Columns JSON
try:
    cols = json.loads(columns)
    if not isinstance(cols, list):
        raise ValueError
except Exception:
    raise ValueError("Columns must be a valid JSON array.")

for col in cols:
    if col not in df.columns:
        print(f"Warning: Column '{{col}}' not found. Skipping.")
        continue

    median_value = df[col].median(skipna=True)
    df[col] = df[col].fillna(median_value)

df.to_csv(output_path, index=False)
print(f"Median imputation complete. Output saved to: {{output_path}}")
"""
]

# Execute the command
subprocess.run(command, check=True)
print(f"CSV file should be available at: {output_csv}")
