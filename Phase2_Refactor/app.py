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
    st.session_state["product_log"] = data_manager.load_data(Path("Phase2_Refactor/product_log.json"))

if "users" not in st.session_state:
    st.session_state["users"] = data_manager.load_data(Path("Phase2_Refactor/users.json"))

if "AI" not in st.session_state:
    st.session_state["AI"] = data_manager.load_data(Path("Phase2_Refactor/AI.json"))

from ui import auth_ui

def log_out():
    st.session_state["logged_in"] = False
    st.session_state["user"] = None
    st.session_state["role"] = None
    st.session_state["page"] = "login"
    st.rerun()

if not st.session_state["logged_in"]:
    auth_ui.log_in()
    auth_ui.reg_render("Phase2_Refactor/users.json")

#Owner
elif st.session_state["role"] == "Owner":
    if st.session_state["page"] == "home":
        st.markdown("Welcome! This is the Owner dashboard")

    elif st.session_state["page"] == "dashboard":

        if st.session_state["employee_dashboard_view"] == "adding product":
            auth_ui.New_Product("Phase2_Refactor/inventory.json")

        if st.session_state["employee_dashboard_view"] == "updating price":
            auth_ui.Update("Phase2_Refactor/inventory.json")

        if st.session_state["employee_dashboard_view"] == "inventory refill":
            auth_ui.Restock("Phase2_Refactor/inventory.json")

        if st.session_state["employee_dashboard_view"] == "discard item":
            auth_ui.Delete("Phase2_Refactor/inventory.json")

        if st.session_state["employee_dashboard_view"] == "ai for owner":
            auth_ui.AI_Owner("Phase2_Refactor/AI.json")

#Employee
elif st.session_state["role"] == "Employee":
    if st.session_state["page"] == "home":
        st.markdown("Welcome! This is the Employee dashboard!")

    elif st.session_state["page"] == "dashboard":

        if st.session_state["employee_dashboard_view"] == "catalog":
            auth_ui.Cat()

        if st.session_state["employee_dashboard_view"] == "inventory":
            auth_ui.Inv()

        if st.session_state["employee_dashboard_view"] == "rev":
            auth_ui.Revenue("Phase2_Refactor/inventory.json")

        if st.session_state["employee_dashboard_view"] == "ai for employee":
            auth_ui.AI_employee("Phase2_Refactor/AI.json")


with st.sidebar:
    st.subheader("**Account Info**")
    if st.session_state["logged_in"] == True:
        user = st.session_state["user"]
        st.markdown(f"User Email: {user['email']}")
        st.markdown(f"Logged In as: {user['role']}")

        #Employee
        if user["role"] == "Employee":
            if st.button("Current Catalog", type="secondary", use_container_width=True):
                st.session_state["page"] = "dashboard"
                st.session_state["employee_dashboard_view"] = "catalog"
                st.rerun()
        
        if user["role"] == "Employee":
            if st.button("Inventory", type="secondary", use_container_width=True):
                st.session_state["page"] = "dashboard"
                st.session_state["employee_dashboard_view"] = "inventory"
                st.rerun()

        if user["role"] == "Employee":
            if st.button("Daily Sales", type="secondary", use_container_width=True):
                st.session_state["page"] = "dashboard"
                st.session_state["employee_dashboard_view"] = "rev"
                st.rerun()

        if user["role"] == "Employee":
            if st.button("AI Chatbot", type="secondary", use_container_width=True):
                st.session_state["page"] = "dashboard"
                st.session_state["employee_dashboard_view"] = "ai for employee"
                st.rerun()

        #Owner
        if user["role"] == "Owner":
            if st.button("Add New Product", type="secondary", use_container_width=True):
                st.session_state["page"] = "dashboard"
                st.session_state["employee_dashboard_view"] = "adding product"
                st.rerun()

        if user["role"] == "Owner":
            if st.button("Update Prices", type="secondary", use_container_width=True):
                st.session_state["page"] = "dashboard"
                st.session_state["employee_dashboard_view"] = "updating price"
                st.rerun()

        if user["role"] == "Owner":
            if st.button("Restock Inventory", type="secondary", use_container_width=True):
                st.session_state["page"] = "dashboard"
                st.session_state["employee_dashboard_view"] = "inventory refill"
                st.rerun()

        if user["role"] == "Owner":
            if st.button("Delete Discontinued Item(s)", type="secondary", use_container_width=True):
                st.session_state["page"] = "dashboard"
                st.session_state["employee_dashboard_view"] = "discard item"
                st.rerun()

        if user["role"] == "Owner":
            if st.button("AI Chatbot", type="secondary", use_container_width=True):
                st.session_state["page"] = "dashboard"
                st.session_state["employee_dashboard_view"] = "ai for owner"
                st.rerun()

        #Logout for both users
        if st.button("Log out", type="primary", use_container_width=True):
            log_out()
