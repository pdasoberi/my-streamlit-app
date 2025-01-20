import streamlit as st
import streamlit_authenticator as stauth

# Example credentials (use your hashed passwords from config.yaml)
credentials = {
    "usernames": {
        "john_doe": {
            "name": "John Doe",
            "password": "$2b$12$W6H9W6K9df2bsGKgPB1S5uwGaM4ppUedVFYsciz7.uR7erlnYJ6de",
        }
    }
}

authenticator = stauth.Authenticate(credentials, "my_app", "abcdef", cookie_expiry_days=30)

# Login form
name, authentication_status, username = authenticator.login("Login", location="sidebar")

if authentication_status:
    st.write(f"Welcome *{name}*")
elif authentication_status == False:
    st.error("Username/password is incorrect")
elif authentication_status == None:
    st.warning("Please enter your username and password")
