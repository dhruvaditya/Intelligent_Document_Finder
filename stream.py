import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
authenticator.login()

if st.session_state["authentication_status"]:
    authenticator.logout()
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title("✔ Intelligent Document Finder, powered by LlamaIndex 🏆💬🦙")
    st.info("Made with ❤ by Aditya Raj", icon="👩‍💻")
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')

try:
    email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(preauthorization=False)
    if email_of_registered_user:
        st.success('User registered successfully')
except Exception as e:
    st.error(e)


with open('./config.yaml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)