import subprocess
import sys
import os

# --- Configuration: replace these with your MongoDB details ---
input_csv = "train_data.csv"       # Input CSV file path
label_column = "Outcome"          # Label column name
model_path = "output/model.pkl"  # Output model file path

# Ensure output directory exists
os.makedirs(os.path.dirname(model_path), exist_ok=True)

venv_python = sys.executable  # This points to the currently active Python in venv

# --- Run the YAML component logic via Python subprocess ---
command = [
    venv_python,
    "-c",
    f"""
import json
import pandas
import pickle
from sklearn import linear_model
import os

input_csv = '{input_csv}'
label_column_name = '{label_column}'
model_path = '{model_path}'
penalty = 'l2'  # You can modify this as needed
solver = 'lbfgs'  # You can modify this as needed
max_iterations = 100  # You can modify this as needed
multi_class_mode = "auto" # auto, ovr, multinomial
random_seed = 0 

df = pandas.read_csv(input_csv)
model = linear_model.LogisticRegression(
    penalty=penalty,
    #dual=False,
    #tol=1e-4,
    #C=1.0,
    #fit_intercept=True,
    #intercept_scaling=1,
    #class_weight=None,
    random_state=random_seed,
    solver=solver,
    max_iter=max_iterations,
    multi_class=multi_class_mode,
    #l1_ratio=None,
    verbose=1,
)

model_parameters = model.get_params()
model_parameters_json = json.dumps(model_parameters, indent=2)
print("Model parameters:")
print(model_parameters_json)
print()

model.fit(
    X=df.drop(columns=label_column_name),
    y=df[label_column_name],
)

with open(model_path, "wb") as f:
    pickle.dump(model, f)

print(f"Model saved to: {model_path}")
"""
]

# Execute the command
subprocess.run(command, check=True)
print(f"Model should be available at: {model_path}")
