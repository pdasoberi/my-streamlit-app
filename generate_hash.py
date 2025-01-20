import streamlit_authenticator as stauth

# List of passwords you want to hash
passwords = ['2024Hash']  # Replace this with the actual password you want to hash

# Hash the passwords
hashed_passwords = stauth.Hasher(passwords).generate()

# Print the hashed password(s)
print(hashed_passwords[0])  # If you have multiple passwords, adjust as needed
