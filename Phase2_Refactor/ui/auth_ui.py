import streamlit as st
from services.test_services import user_auth, registration
import time
from data import data_manager
from pathlib import Path
  

def log_in():
    st.subheader("Log In")
    with st.container(border=True):
        email_input = st.text_input("Email", key="email_login")
        password_input = st.text_input("Password", type="password", key="password_login")
        if st.button("Log In", type="primary", use_container_width=True):
            
            with st.spinner("Logging in..."):
                time.sleep(2)
                users = st.session_state["users"]
                found_user = user_auth(users, email_input, password_input)

                if found_user:
                    st.success(f"Welcome back, {found_user['email']}!")
                    st.session_state["logged_in"] = True
                    st.session_state["user"] = found_user
                    st.session_state["role"] = found_user["role"]
                    st.session_state["page"] = "home"

                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("Invalid credentials")

def reg_render(file : str):
    users = st.session_state["users"]

    st.subheader("Register a New Account")
    with st.container(border=True):
        new_email = st.text_input("Email", key="email_register")
        new_password = st.text_input("Password", type="password", key="password_edit")

        user_role = ["", "Owner", "Employee"]
        new_role = st.selectbox("Role", user_role)


        if st.button("Create Account", key= "register_btn"):
            #+
            reg_errors = registration(users, new_email, new_password, new_role)
                
            if reg_errors:
                for invalid in reg_errors:
                    st.error(invalid)
            else:
                data_manager.save_data(file, users)
                st.success("Account created!")
                time.sleep(1)
                st.rerun()
                
        st.write("---")
        st.dataframe(users)
