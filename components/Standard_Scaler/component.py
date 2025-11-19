import subprocess
import sys
import os

# --- Configuration: replace these with your MongoDB details ---
input_csv = "test_data.csv"       # Input CSV file path
columns = '["Pregnancies", "Glucose", "BloodPressure", "BMI","Insulin","SkinThickness", "DiabetesPedigreeFunction", "Age"]'  # Columns to process as JSON array string
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
import numpy as np
from pathlib import Path
from sklearn.preprocessing import StandardScaler
import os

input_csv = '{input_csv}'
output_path = '{output_csv}'
columns = '{columns}'

df = pd.read_csv(input_csv)
# Parse JSON array
try:
    cols = json.loads(columns)
    if not isinstance(cols, list):
        raise ValueError
except Exception:
    raise ValueError("Columns must be a valid JSON array.")

missing_cols = [c for c in cols if c not in df.columns]
if missing_cols:
    print(f"Warning: Columns not found: {{missing_cols}}. They will be skipped.")

scaler = StandardScaler()

valid_cols = [c for c in cols if c in df.columns]

if not valid_cols:
    print("No valid columns found for scaling. Copying input to output.")
    df.to_csv(output_path, index=False)
    exit(0)

df[valid_cols] = scaler.fit_transform(df[valid_cols])

df.to_csv(output_path, index=False)
print(f"Standard scaling applied. Output saved to: {{output_path}}")
"""
]

# Execute the command
subprocess.run(command, check=True)
print(f"CSV file should be available at: {output_csv}")
