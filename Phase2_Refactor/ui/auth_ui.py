import streamlit as st
from services.test_services import user_auth, registration
from services.owner_services import Add_new_product, Update_prices, Restock_Inv, del_discontinued_items
from services.employee_services import current_cat, inv, daily_sales, ded_inv
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

#Owner
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

def Restock(file:str):
    # Section 3: Restock (Update)
    inventory = st.session_state["inventory"]
    st.header("Restock Inventory")
    with st.container(border=True):
        if not inventory:
            st.warning("No inventory available to restock")

        else:
            item_selected = [item["name"] for item in inventory]
            Select_Name = st.selectbox("Select an item to restock", item_selected)
            selected_item = Restock_Inv(inventory, Select_Name)


            Restock_Quantity = st.number_input("Restock Quantity", min_value=1, step=1)

            if selected_item:
                st.write(f"Current stock: {selected_item['stock']}")

            if st.button("Restock"):
                if selected_item is None:
                    st.error("Please select an item")
                else:
                    selected_item["stock"] += Restock_Quantity


                    data_manager.save_data(file, inventory)
                    st.success(f"{selected_item['name']} is successfully restocked")
                    st.success(f"New Stock: {selected_item['stock']}")
                    time.sleep(1)
                    st.rerun()

def Delete(file:str):
    # Section 4: Deleting Discontinued Items (Delete/Cancel)
    inventory = st.session_state["inventory"]
    st.header("Delete Discontinued Item(s)")
    with st.container(border=True):
        if not inventory:
            st.warning("No inventory available to delete")
            return

        product_names = []
        for dis_item in inventory:
            product_names.append(dis_item["name"])
        Selected_dis_product = st.selectbox("Select the discontinued item", product_names)

        discontinued_name = {}
        for dis_item in inventory:
            if dis_item["name"] == Selected_dis_product:
                discontinued_name = dis_item
                break
                
        if discontinued_name:
            st.write("### Selected Item Details:")
            st.write(f"**Item ID**: {discontinued_name['id']}")
            st.write(f"**Name**: {discontinued_name['name']}")
            st.write(f"**Category**: {discontinued_name['category']}")
            st.write(f"**Price**: {discontinued_name['price']}")
            st.write(f"**Stock**: {discontinued_name['stock']}")

            btn_delete = st.button("Delete Item")

            if btn_delete:
                deleted_item = del_discontinued_items(inventory, Selected_dis_product)

                if deleted_item:
                    data_manager.save_data(file, inventory)
                    st.success(f"{Selected_dis_product} was deleted successfully")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Item could not be found")

#Employee
# Employee Catalog
def Cat():
    inventory = st.session_state["inventory"]
    st.header("Current Catalog")
    with st.container(border=True):
        # Search functionality using `current_cat` from employee_services
        search = st.text_input("Search", placeholder="Filter items by name")
        viewing_inventory = current_cat(inventory, search)

        # Store the filtered inventory in session state
        st.session_state["viewing_inventory"] = viewing_inventory

        # Display the filtered inventory
        if viewing_inventory:
            st.subheader("Current Inventory")
            st.dataframe(viewing_inventory, use_container_width=True)

            # Display total stock
            total_stock = sum(item.get("stock", 0) for item in viewing_inventory)
            st.metric("Total Stock", total_stock)
        else:
            st.error("No item(s) found, please try again.")

# Employee Inventory
def Inv():
    viewing_inventory = st.session_state.get("viewing_inventory", st.session_state["inventory"])
    st.header("Inventory Overview")
    with st.container(border=True):
        if viewing_inventory:
            # Display the full inventory
            st.dataframe(viewing_inventory, use_container_width=True)

            # Display low-stock items using `inv` from employee_services
            low_stock_items = inv(viewing_inventory, threshold=10)
            if low_stock_items:
                st.warning("Low Stock on the following item(s):")
                st.dataframe(low_stock_items, use_container_width=True)
            else:
                st.success("All items are sufficiently stocked.")
        else:
            st.error("No inventory available.")

def Revenue(file: str):
    inventory = st.session_state["inventory"]
    product_log = st.session_state["product_log"]
    viewing_inventory = st.session_state.get("viewing_inventory", inventory)
    st.header("Daily Sales")
    with st.connection(border=True):
        matching_products = []

        for product in product_log:
            for item in viewing_inventory:
                if product ["Item"] == item["name"]:
                    matching_products.append(product)
                    break

        if matching_products:
            st.dataframe(matching_products, use_container_width=True)
        else:
            st.info("No product found for matching item(s).")

    with st.container(border=True):
        st.header("Deduct from Inventory")

        sold_items = []
        for sold in product_log:
            sold_items.append("Select sold item", sold_items)

        Sel_Name = st.selectbox("Select sold item", sold_items)

        sel_sale = None
        for sale in product_log:
            if sale["Item"] == Sel_Name:
                sel_sale =sale
                break
        
        sel_inv = None
        for item in inventory:
            if item ["name"] == Sel_Name:
                sel_inv = item
                break
        
        if sel_sale and sel_inv:
            st.write(f"Quantity Sold: {sel_sale['Amount sold']}")
            st.write(f"Current Inventory: {sel_inv['stock']}")

            if st.button("Edit Inventory"):
                sel_inv["stock"] -= sel_sale["Amount sold"]

                data_manager.save_data(file, inventory)

                st.success("Inventory Updated")
                st.write(f"New Inventory: {sel_inv['sstock']}")
                time.sleep(3)
                st.rerun
        else:
            st.error("Unable to find an item that matches the Inventory or Product Log.")
