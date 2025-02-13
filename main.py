import joblib
import traceback
from utils import classify_password, sanitize_input


file_path = "data/rockyou.txt"

try:
    rf_model = joblib.load("rf_model.pk1")
    model_columns = joblib.load("model_columns.pk1")
    print("Model and columns loaded successfully.")
except FileNotFoundError as e:
    exit(1)
while True:
    try:
        print("Ready to accept input...")
        user_password = sanitize_input(input("Enter a password to test: "))
        if user_password.lower() == 'exit':
            break

        prediction = classify_password(rf_model, user_password, model_columns)
        print(f"Predicted Strength: {['Weak', 'Average', 'Strong'][prediction]}")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print("An unexpected error occurred. Please try again")
        traceback.print_exc()

