import pandas
from feature_engineering import is_in_dictionary

def classify_password(rf_model, user_password, X_train_columns):
    # Get the features from the user password
    user_features = {
            'password_length' : len(user_password),
            'length' : len(user_password),
            'numDigits' : sum(c.isdigit() for c in user_password),
            'numUpperCase' : sum(c.isupper() for c in user_password),
            'numLowerCase' : sum(c.islower() for c in user_password),
            'numSpecial': sum(not c.isalnum() for c in user_password),
            'isInDictionary': is_in_dictionary(user_password),
        }

    print(f"Extracted features : {user_features}")

    user_features_df = pandas.DataFrame([user_features])
    user_features_df = user_features_df.reindex(columns=X_train_columns, fill_value=0)

    prediction = rf_model.predict(user_features_df)[0]
    return prediction

def sanitize_input(user_input):
    if not user_input or len(user_input) > 128:
        raise ValueError("Invalid password length.")
    if not all (c.isprintable() for c in user_input):
        raise ValueError("Password contains unprintable characters.")
    return user_input.strip()