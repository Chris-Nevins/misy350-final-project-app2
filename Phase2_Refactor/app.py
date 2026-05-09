import streamlit as st
from pathlib import Path
from data import data_manager

st.set_page_config(page_title="Precision Hardware", layout="centered")
st.title("Precision Hardware")

if "inventory" not in st.session_state:

    st.session_state["inventory"] = data_manager.load_data(Path("Phase2_Refactor/inventory.json"))

if "product_log" not in st.session_state:
    st.session_state["product_log"] = data_manager.load_data(Path("Phase2_Refactor/product.json"))

if "users" not in st.session_state:
    st.session_state["users"] = data_manager.load_data(Path("Phase2_Refactor/users.json"))

from ui import auth_ui
auth_ui.log_in()
auth_ui.reg_render("Phase2_Refactor/users.json")