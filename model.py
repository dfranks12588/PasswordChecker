from collections import Counter
import joblib
from sklearn.ensemble import  RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from imblearn.over_sampling import SMOTE



def train_model(X, Y, class_weights):
    print("DEBUG: Training process invoked")

    # Splitting the data into training and testing sets
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    # Using SMOTE to address the class imbalance (Excess weak passwords in the dataset)
    smote = SMOTE(sampling_strategy={0: 50000, 1: 50000, 2:10000}, random_state=42)
    X_resampled, Y_resampled = smote.fit_resample(X_train, Y_train)

    print(f"Resampled dataset class distro: {Counter(Y_resampled)}")

    # Train the Random Forest model
    rf_model = RandomForestClassifier(n_estimators=75, max_depth=20, class_weight=class_weights, random_state=42, n_jobs=-1)
    rf_model.fit(X_resampled, Y_resampled)


    return rf_model, X_train, Y_train

# This is being used to retrain the model to integrate a check for dictionary words.
def retrain_model(file_path, save_model=True):
    from data_loader import load_password_data
    from feature_engineering import extract_features

    password_df = load_password_data(file_path)
    password_df = extract_features(password_df)

    X = password_df.drop(columns=['strength'])
    Y = password_df['strength']

    class_weights = {cls: len(Y) / (3 * count) for cls, count in Counter(Y).items()}

    rf_model, X_train, Y_train = train_model(X, Y, class_weights)

    if save_model:
        joblib.dump(rf_model, "rf_model.pk1")
        joblib.dump(X_train.columns.tolist(), "model_columns.pk1")
        print("Model and feature columns saved!")
    return rf_model

