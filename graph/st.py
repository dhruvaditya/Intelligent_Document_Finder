import streamlit as st
import jwt
import datetime
from hashlib import sha256

# Secret key for JWT encoding and decoding
SECRET_KEY = "your_secret_key_here"

def generate_token(username):
    # Token expires in 30 minutes
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    token = jwt.encode({'username': username, 'exp': expiration_time}, SECRET_KEY, algorithm='HS256')
    return token

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['username']
    except jwt.ExpiredSignatureError:
        st.error('Token has expired, please log in again.')
        return None
    except jwt.InvalidTokenError:
        st.error('Invalid token, please log in again.')
        return None

def hash_password(password):
    return sha256(password.encode()).hexdigest()

# Dummy user database
users_db = {
    "john_doe": {
        "username": "john_doe",
        "password_hash": hash_password("password123"),  # Never store passwords in plain text
    }
}

def login(username, password):
    user = users_db.get(username)
    if user and user['password_hash'] == hash_password(password):
        token = generate_token(username)
        st.session_state['token'] = token
        st.session_state['username'] = username
        st.success('Logged in successfully!')
    else:
        st.error('Invalid username or password')

def logout():
    if 'token' in st.session_state:
        del st.session_state['token']
        del st.session_state['username']
    st.info('Logged out.')

# UI for login
if 'token' not in st.session_state:
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            login(username, password)

# UI for logout
if 'token' in st.session_state:
    if st.button('Logout'):
        logout()

# Protected content
if 'token' in st.session_state:
    username = verify_token(st.session_state['token'])
    if username:
        st.write(f"Welcome {username}! You are viewing protected content.")
