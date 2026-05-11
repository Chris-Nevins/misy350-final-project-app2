import streamlit as st
from pathlib import Path
from data import data_manager

st.set_page_config(page_title="Precision Hardware", layout="centered")
st.title("Precision Hardware")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "user" not in st.session_state:
    st.session_state["user"] = None

if "role" not in st.session_state:
    st.session_state["role"] = None

if "page" not in st.session_state:
    st.session_state["page"] = "login"

#JSON
if "inventory" not in st.session_state:
    st.session_state["inventory"] = data_manager.load_data(Path("Phase2_Refactor/inventory.json"))

if "product_log" not in st.session_state:
    st.session_state["product_log"] = data_manager.load_data(Path("Phase2_Refactor/product.json"))

if "users" not in st.session_state:
    st.session_state["users"] = data_manager.load_data(Path("Phase2_Refactor/users.json"))

from ui import auth_ui

if not st.session_state["logged_in"]:
    auth_ui.log_in()
    auth_ui.reg_render("Phase2_Refactor/users.json")

#Owner
elif st.session_state["role"] == "Owner":
    if st.session_state["page"] == "home":
        st.markdown("Welcome! This is the Owner dashboard")
        if st.button("Go to Dashboard", key= "dashboard_view_btn", type= "primary", use_container_width=True):
            st.session_state["page"] = "dashboard"
            st.rerun()
    elif st.session_state["page"] == "dashboard":
        st.markdown("Dashboard")    

        if st.button("Log out", type="primary", width='content'):
            st.session_state["logged_in"] = False
            st.session_state["user"] = None
            st.session_state["role"] = None
            st.session_state["page"] = "login"
            import time
            time.sleep(4)
            st.rerun()

        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Add New Product", "Update Prices", "Restocking", "Deleting", "AI Chatbot"])    

        with tab1:
            auth_ui.New_Product("Phase2_Refactor/inventory.json")

        with tab2:
            auth_ui.Update("Phase2_Refactor/inventory.json")

        with tab3:
            auth_ui.Restock("Phase2_Refactor/inventory.json")

        with tab4:
            auth_ui.Delete("Phase2_Refactor/inventory.json")

        with tab5:
            pass

#Employee
elif st.session_state["role"] == "Owner":
    if st.session_state["page"] == "home":
        st.markdown("Welcome! This is the Owner dashboard")
        if st.button("Go to Dashboard", key= "dashboard_view_btn", type= "primary", use_container_width=True):
            st.session_state["page"] = "dashboard"
            st.rerun()
    elif st.session_state["page"] == "dashboard":
        st.markdown("Dashboard")    

        if st.button("Log out", type="primary", width='content'):
            st.session_state["logged_in"] = False
            st.session_state["user"] = None
            st.session_state["role"] = None
            st.session_state["page"] = "login"
            import time
            time.sleep(4)
            st.rerun()

        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Add New Product", "Update Prices", "Restocking", "Deleting", "AI Chatbot"])    

        with tab1:
            auth_ui.New_Product("Phase2_Refactor/inventory.json")

        with tab2:
            auth_ui.Update("Phase2_Refactor/inventory.json")

        with tab3:
            auth_ui.Restock("Phase2_Refactor/inventory.json")

        with tab4:
            auth_ui.Delete("Phase2_Refactor/inventory.json")

        with tab5:
            pass
