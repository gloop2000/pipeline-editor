import subprocess
import sys
import os

# --- Configuration: replace these with your MongoDB details ---
input_csv = "test_data.csv"       # Input CSV file path
testSize = 0.2                     # Proportion of data to use as test set
randomState = 42                  # Random seed for reproducibility
output_test_csv = "output/test_data.csv"       # Output CSV file path
output_train_csv = "output/train_data.csv"     # Output CSV file path

# Ensure output directory exists
os.makedirs(os.path.dirname(output_train_csv), exist_ok=True)

venv_python = sys.executable  # This points to the currently active Python in venv

# --- Run the YAML component logic via Python subprocess ---
command = [
    venv_python,
    "-c",
    f"""
import pandas as pd
from sklearn.model_selection import train_test_split
from pathlib import Path

input_path = '{input_csv}'
test_size = '{testSize}'
random_state = '{randomState}'
test_path = '{output_test_csv}'
train_path = '{output_train_csv}'

df = pd.read_csv(input_path)

try:
    test_size = float(test_size)
    if not (0 < test_size < 1):
        raise ValueError
except Exception:
    raise ValueError("Test Size must be a float between 0 and 1.")

try:
    random_state = int(random_state)
except Exception:
    raise ValueError("Random State must be an integer.")

train_df, test_df = train_test_split(
    df,
    test_size=test_size,
    random_state=random_state,
    shuffle=True
)

train_df.to_csv(train_path, index=False)
test_df.to_csv(test_path, index=False)

print(f"Train samples: {{len(train_df)}}, Test samples: {{len(test_df)}}")
print(f"Train saved to: {{train_path}}")
print(f"Test saved to: {{test_path}}")
"""
]

# Execute the command
subprocess.run(command, check=True)
print(f"CSV file should be available at: {{output_csv}}")
