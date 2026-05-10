import streamlit as st
from services.test_services import user_auth, registration
from services.owner_services import Add_new_product, Update_prices
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

def New_Product(file: str):
    # Section 1: Add New Product (Create)
    inventory = st.session_state["inventory"]
    st.header("Add New Product")
    with st.container(border=True):
        # Item ID
        New_ID = st.number_input("Set an Unique Numerical ID", step = 1.0, format="%.f")

        # Item Name
        New_Item_Name = st.text_input("Name")

        # Item Category
        Current_Cat = ["","GPU", "Memory", "Motherboard", "Processor", "Power Supply", "Case", "Cooling", "Networking"]
        New_Cat = st.selectbox("Category", Current_Cat)

        # Item Price
        New_Price = st.number_input("Insert Price", min_value=0.0, step=1.0, format="%.2f")

        # Item Stock
        New_Stock = st.number_input("Amount to inventory", min_value=0.0, step=1.0, format="%.f") 


        if st.button("Submit Change"):

            errors = Add_new_product(inventory, New_ID, New_Item_Name, New_Cat, New_Price, New_Stock)
            if errors:
                for error in errors:
                    st.error(error)
            else:
                data_manager.save_data(file, inventory)
                st.success("New Product Added")
                time.sleep(1)
                st.rerun()

def Update(file:str):
    # Section 2: Update Prices (Read)
    inventory = st.session_state["inventory"]
    st.header("Update Prices")
    with st.container(border=True):
        search = st.text_input("Search", placeholder= "filter items by name")
        filtered_inventory = Update_prices(inventory, search)
        
        if len(filtered_inventory) == 1:
            selected_item = filtered_inventory[0]

            new_price = st.number_input(
                        f"Set new price for {selected_item['name']}",
                        min_value=0.0,value=float(selected_item["price"]),step=1.0)

            if st.button("Update Price"):
                selected_item["price"] = new_price

                data_manager.save_data(file, inventory)
                st.success(f"Price for {selected_item['name']} updated to ${new_price:.2f}")
                time.sleep(1)
                st.rerun()

    if filtered_inventory:
        st.subheader("Current Inventory")
        st.dataframe(filtered_inventory, use_container_width= True)

    else:
        st.error("No item(s) found please try again")
