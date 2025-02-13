import joblib
import os
from collections import Counter
from feature_engineering import extract_features
from data_loader import  load_password_data
from model import train_model
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import cross_val_score

def main():
    DEBUG = True

    file_path = os.getenv("DATA_FILE_PATH", "data/rockyou.txt")

    sample_size = 100000 if DEBUG else None

    password_df = load_password_data(file_path, sample_size=sample_size)
    password_df = extract_features(password_df)

    X = password_df.drop(columns=['strength'])
    Y = password_df['strength']

    class_counts = Counter(Y)
    total_samples = len(Y)
    num_classes = len(class_counts)
    class_weights = {cls: total_samples / (num_classes * count) for cls, count in class_counts.items()}

    #Training the model
    rf_model, X_train, Y_train = train_model(X, Y, class_weights)

    # Evaluating the model on the test data set
    print("\nEvaluating the model: ")
    Y_prediction = rf_model.predict(X_train)

    #Confusion matrix
    print("\nConfusion Matrix")
    print(confusion_matrix(Y_train, Y_prediction))

    #Classification Report
    print("\nClassification Report: ")
    print(classification_report(Y_train, Y_prediction, target_names=["Weak", "Average", "Strong"]))

    # Cross-validation accuracy
    scores = cross_val_score(rf_model, X, Y, cv=5, scoring='accuracy')
    print(f"Cross validation accuracy: {scores.mean():.2f}")
    print(f"Cross validation scores: {scores}")
    print(f"Mean cross-val score: {scores.mean()}")


    joblib.dump(rf_model, "rf_model.pk1")
    joblib.dump(X_train.columns, "model_columns.pk1")
if __name__=="__main__":
    main()