import subprocess
import sys
import os

# --- Configuration: replace these with your MongoDB details ---
input_csv = "test_data.csv"       # Input CSV file path
label_column = "Outcome"          # Label column name
model_path = "model.pkl"  # Output model file path
predictions_path = "output/predictions.csv"  # Output predictions file path

# Ensure output directory exists
os.makedirs(os.path.dirname(predictions_path), exist_ok=True)

venv_python = sys.executable  # This points to the currently active Python in venv

# --- Run the YAML component logic via Python subprocess ---
command = [
    venv_python,
    "-c",
    f"""
import pandas
import pickle

model_path = '{model_path}'
dataset_path = '{input_csv}'
predictions_path = '{predictions_path}'
label_column_name = '{label_column}'

# Load model
with open(model_path, "rb") as f:
    model = pickle.load(f)

df = pandas.read_csv(dataset_path)
df = df.drop(columns=[label_column_name])

# Predict class labels
y_pred = model.predict(df)

# Predict probabilities (if available)
try:
    y_proba = model.predict_proba(df)
    has_proba = True
except Exception:
    has_proba = False

# Prepare output dataframe
output = pandas.DataFrame()
output["prediction"] = y_pred

if has_proba:
    for i in range(y_proba.shape[1]):
        output[f"probability_class_{{i}}"] = y_proba[:, i]

output.to_csv(predictions_path, index=False)
print(f"Predictions saved to: {{predictions_path}}")
"""
]

# Execute the command
subprocess.run(command, check=True)
print(f"Predictions should be available at: {predictions_path}")
