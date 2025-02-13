import pandas

def load_password_data(file_path, sample_size=None):
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