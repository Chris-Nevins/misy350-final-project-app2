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
elif st.session_state["role"] == "Employee":
    if st.session_state["page"] == "home":
        st.markdown("Welcome! This is the Employee dashboard")
        if st.button("Go to Dashboard", key="dashboard_view_btn", type="primary", use_container_width=True):
            st.session_state["page"] = "dashboard"
            st.rerun()
    elif st.session_state["page"] == "dashboard":
        st.markdown("Dashboard")

        if st.button("Log out", type="primary", use_container_width=True):
            st.session_state["logged_in"] = False
            st.session_state["user"] = None
            st.session_state["role"] = None
            st.session_state["page"] = "login"
            import time
            time.sleep(4)
            st.rerun()

        # Define tabs for the employee dashboard
        tab1, tab2, tab3, tab4 = st.tabs(["Catalog", "Inventory", "Daily Sales", "Matching Products"])

        # Catalog Tab
        with tab1:
            st.subheader("Current Catalog")
            search = st.text_input("Search Inventory", placeholder="Filter items by name")
            filtered_inventory = current_cat(st.session_state["inventory"], search)

            if filtered_inventory:
                st.dataframe(filtered_inventory, use_container_width=True)
            else:
                st.error("No items match your search.")

        # Inventory Tab
        with tab2:
            st.subheader("Inventory Overview")
            total_stock = sum(item.get("stock", 0) for item in st.session_state["inventory"])
            st.metric("Total Stock", total_stock)

            low_stock_items = inv(st.session_state["inventory"], threshold=5)
            if low_stock_items:
                st.warning("Low Stock on the following item(s):")
                st.dataframe(low_stock_items, use_container_width=True)
            else:
                st.success("All items are sufficiently stocked.")

        # Daily Sales Tab
        with tab3:
            st.subheader("Daily Sales")
            today_sales = daily_sales(st.session_state["product_log"])

            if today_sales:
                st.dataframe(today_sales, use_container_width=True)
            else:
                st.info("No sales recorded for today.")

        # Matching Products Tab
        with tab4:
            st.subheader("Matching Products")
            matching_products = match_products_with_inventory(
                st.session_state["product_log"], st.session_state["inventory"]
            )

            if matching_products:
                st.dataframe(matching_products, use_container_width=True)
            else:
                st.info("No matching products found.")
