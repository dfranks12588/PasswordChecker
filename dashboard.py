import time
import joblib
import streamlit as st
from feature_engineering import extract_features
from data_loader import load_password_data
import altair
from utils import sanitize_input, classify_password
import pandas

#Caching functions for faster load times
@st.cache_data
def load_password_data_cached():
    start = time.time()
    data = load_password_data()
    sample_size = min(100000, len(data))
    data = data.sample(n=sample_size, random_state=42)
    st.write(f"Data loaded in {time.time() - start:.2f} seconds")
    return data

@st.cache_data
def extract_features_cached(password_df):
    start = time.time()
    features = extract_features(password_df)
    st.write(f"Features extracted in {time.time() - start:.2f} seconds")
    return features

st.set_page_config(page_title="Password Strength Checker", layout="wide")
st.markdown("""
            <style>
            .stButton>button {
            background-color: #1db954;
            color: white;
            border-radius: 8px;
            }
            </style>"""
            , unsafe_allow_html=True)

#Load the model and feature columns
rf_model = joblib.load("rf_model.pk1")
model_columns = joblib.load("model_columns.pk1")

#Load and preprocess data
password_df = load_password_data_cached()
password_df = extract_features_cached(password_df)

st.title("Password Strength Checker Dashboard")
st.markdown("This dashboard allows users to explore password data and test potential password strength, as well as "
            "view model insights")

st.header("Data Overview")
#Password Strength Distribution visualization

st.subheader("Password Strength Distribution")
strength_labels = {0: "Weak", 1: "Average", 2: "Strong"}
class_counts = password_df['strength'].value_counts()
class_counts = class_counts.rename(index=strength_labels).reset_index()
class_counts.columns = ["Password Strength", "Count"]

strength_chart = altair.Chart(class_counts).mark_bar(color="blue").encode(
    x=altair.X("Password Strength:N", title="Password Strength", sort=["Weak", "Average", "Strong"]),
    y=altair.Y("Count:Q", title="Count"),
    tooltip=["Password Strength", "Count"]
).properties(
    title="Password Strength Distribution(Sorted)",
    width=700,
    height=400
)
st.altair_chart(strength_chart, use_container_width=True)

#Feature Importance visualization
st.subheader("Feature Importance")
feature_importance = rf_model.feature_importances_
feature_names = model_columns
feature_importance = pandas.DataFrame({
    "Feature": feature_names,
    "Importance": feature_importance
}).sort_values(by="Importance", ascending=False)
feature_chart = altair.Chart(feature_importance).mark_bar(color="green").encode(
    x=altair.X("Feature", sort="-y", title="Features"),
    y=altair.Y("Importance", title="Importance"),
    tooltip=["Feature", "Importance"]
).properties(
    title="Feature Importance",
    width=700,
    height=400
)
st.altair_chart(feature_chart, use_container_width=True)

#Password length distribution visualization
st.subheader("Password Length Distribution")
password_df['password_length'] = password_df['length']
password_lengths = password_df[password_df['password_length'] <=50]['password_length'].value_counts().reset_index()
password_lengths.columns = ['Password Length', 'Frequency']

length_chart = altair.Chart(password_lengths).mark_bar(color="red").encode(
    x=altair.X("Password Length:Q", title="Password Length"),
    y=altair.Y("Frequency:Q", title="Frequency"),
    tooltip=["Password Length", "Frequency"]
).properties(
    title="Password Length Distribution (Limited to 50)",
    width=700,
    height=400
)
st.altair_chart(length_chart, use_container_width=True)

st.header("Test Password Strength")
user_password = st.text_input("Enter a password: ")
if user_password:
    sanitized_password = sanitize_input(user_password)
    prediction = classify_password(rf_model, sanitized_password, model_columns)

    prediction_mapping = {0: "Weak", 1: "Average", 2: "Strong"}
    prediction_label = prediction_mapping.get(prediction, "Unknown")

    st.success(f"The predicted strength is: **{prediction_label}**")

    password_features = extract_features(pandas.DataFrame({"password": [user_password]})).iloc[0]
    recommendations = []

    if password_features["length"] < 12:
        recommendations.append("Increase the length of your password to at least 12 characters")
    if password_features["numDigits"] < 2:
        recommendations.append("Include at least 2 numbers.")
    if password_features["numSpecial"] < 2:
        recommendations.append("Add at least 2 special characters (!, @, #, etc.).")
    if password_features["numUpperCase"] < 1:
        recommendations.append("Include at least one uppercase letter.")
    if password_features["numLowerCase"] < 1:
        recommendations.append("Include at least one lowercase letter.")
    if password_features["isInDictionary"] == 1:
        recommendations.append("Avoid using common words found in the dictionary.")

    if recommendations:
        st.warning("You can be improved by: ")
        for recommendation in recommendations:
            st.write(f" {recommendation}")
    else:
        st.info("Your password is strong! No further improvments are recommdended.")