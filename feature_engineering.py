import math
import nltk.data
from nltk.corpus import words
from nltk.data import find
import os

project_dir = os.path.dirname(os.path.abspath(__file__))
nltk_data_path = os.path.join(project_dir, "nltk_data")
nltk.data.path.append(nltk_data_path)

try:
    find('corpora/words.zip')
    english_word = set(words.words())
    print("Nltk words loaded successfully")
except LookupError:
    print("Nlkt words not found)")


def calculate_entropy(password):
    probability = [password.count(char) / len(password) for char in set(password)]
    entropy = -sum(p * math.log2(p) for p in probability)
    return entropy / len(password)

#Sorts passwords into Weak,Average, and Strong categories
def password_strength(password):
    if len(password) < 8:
        return "Weak"
    elif password.isalpha() or password.isdigit():
        return "Weak"

    if (
        any(c.islower() for c in password) and
        any(c.isupper() for c in password) and
        any(c.isdigit() for c in password) and
        any(not c.isalnum() for c in password)
    ):
        return "Strong"
    if (
            (any(c.islower() for c in password) or any(c.isupper() for c in password))
            and (any(c.isdigit() for c in password) or any(not c.isalnum() for c in password))
    ):
        return "Average"

    return "Weak"

def is_in_dictionary(password):
    import re

    substrings = re.split(r'\W+|\d+', password.lower())
    for substring in substrings:
        if substring in english_word and len(substring) > 2:
            return 1
        return 0

def extract_features(password_df):
    password_df['strength'] = password_df['password'].apply(password_strength)

    password_df['length'] = password_df['password'].str.len()
    password_df['numDigits'] = password_df['password'].str.count(r'\d')
    password_df['numUpperCase'] = password_df['password'].str.count(r'[A-Z]')
    password_df['numLowerCase'] = password_df['password'].str.count(r'[a-z]')
    password_df['numSpecial'] = password_df['password'].str.count(r'[^\w\s]')
    password_df['entropy'] = password_df['password'].apply(calculate_entropy)
    password_df['isInDictionary'] = password_df['password'].apply(is_in_dictionary)
    password_df['strength'] = password_df['strength'].map({"Weak": 0, "Average": 1, "Strong": 2})
    password_df = password_df.drop(columns=['password'])

    return password_df

