import streamlit as st
#Connect with Postgre SQL  # Will replace with pg admin


# Placeholder functions for user management
def add_user(username, password):
    # logic to add user to the database
    pass

def authenticate_user(username, password):
    # logic to authenticate user
    return True  # actual authentication logic

# Sign-up form
def sign_up_form():
    with st.form("Sign_up"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Sign up")
        
        if submit_button:
            add_user(username, password)  # logic to handle user creation
            st.success("Account created successfully!")

# Login form
def login_form():
    with st.form("Login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            if authenticate_user(username, password):  # logic to verify credentials
                st.session_state["user"] = username  # Create a session
                st.success(f"Welcome {username}!")
            else:
                st.error("Invalid username or password")

# Main app logic
if "user" not in st.session_state:
    # User is not logged in
    st.sidebar.title("Account")
    login_form()
    st.sidebar.write("Not a member?")
    st.sidebar.button("Sign up", on_click=sign_up_form)
else:
    # User is logged in
    st.write(f"Welcome, {st.session_state['user']}!")
    if st.button("Logout"):
        del st.session_state["user"]  # End the session
