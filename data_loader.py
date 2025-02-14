import pandas
import os
import requests



def download_rockyou():

    file_path = "data/rockyou.txt"
    google_drive_id = "1xFzybpd0PTVOwljzHrmxbihLg9ewyQim"

    if not os.path.exists("data"):

        os.makedirs("data")

    if not os.path.exists(file_path):
        print("Downloading rockyou.txt...")
        url = f"https://drive.google.com/uc?id={google_drive_id}&export=download"
        response = requests.get(url, stream=True)

        if response.status_code== 200:
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)
            print("Download complete!")
        else:
            print("Failed to download rockyou.txt")
    return file_path

def load_password_data(sample_size=None):

    file_path = download_rockyou()

    passwords = []
    with open(file_path, 'r', encoding="latin1") as file:
        for line in file:
            line = line.strip()
            if line:
                passwords.append(line)

    # Converts to a DataFrame and removes duplicates
    password_df = pandas.DataFrame(passwords, columns=['password'])

    # Removes duplicates
    password_df = password_df.drop_duplicates()

    if sample_size:
        password_df = password_df.sample(n=sample_size, random_state=42)
    return password_df