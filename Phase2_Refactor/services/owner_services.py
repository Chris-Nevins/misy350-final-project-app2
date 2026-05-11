import uuid
from typing import Optional, List, Dict

def Add_new_product(inventory: list[Dict], New_ID: int, New_Item_Name: str, New_Cat: str, New_Price: float, New_Stock: int):
    errors = []

    # duplicate ID
    for item_id in inventory:
        if New_ID == item_id["id"]:
            errors.append("That ID has already been taken")
            break

    # duplicate name
    for item_name in inventory:
        if New_Item_Name.replace(" ", "").strip().lower() == item_name["name"].replace(" ", "").strip().lower():
            errors.append("That Item already exists, please use restock inventory instead")
            break

    # Confirm empty name
    if New_Item_Name.strip() == "":
        errors.append("Please enter a name")

    # Confirm Category
    if New_Cat == "":
        errors.append("Please select a category")
                            
    # Confirm Price
    if New_Price <= 0:
        errors.append("Please enter a price")

    # Confirm Stock
    if New_Stock <= 0:
        errors.append("Please enter a quantity")

    if errors:
        return errors

    inventory.append({
        "id": int(New_ID),
        "name": New_Item_Name,
        "category": New_Cat,
        "price": float(New_Price),
        "stock": int(New_Stock)
    })

    return []

def Update_prices(inventory: list[Dict], search: str):
    filtered_inventory = []

    if search:
        for item in inventory:
            if search.lower() in item["name"].lower():
                filtered_inventory.append(item)
    else:
        filtered_inventory = inventory
    return filtered_inventory

def Restock_Inv(inventory: list[Dict], Select_Name: str):
    for item in inventory:
        if item["name"] == Select_Name:
            return item

    return None

def del_discontinued_items(inventory: list[Dict], selected_name: str):
    for item in inventory:
        if item["name"] == selected_name:
            inventory.remove(item)
            return item

    return None
