import uuid
from typing import Optional, List, Dict

def user_auth(users: list[Dict], email_input: str, password_input:str):
    for user in users:
        if user["email"].strip().lower() == email_input.strip().lower() and user["password"] == password_input:
            return user
    return None

def registration(users: list[Dict], new_email: str, new_password: str, new_role: str):
    reg_errors = []

    for user in users:
        if new_email.lower() == user["email"].lower():
            reg_errors.append("That email already exists, please login instead")

    if new_email == "":
        reg_errors.append("Please enter your email")

    if new_password == "":
        reg_errors.append("Please enter your password")

    if new_role == "":
        reg_errors.append("Please enter a role")

    if reg_errors:
        return reg_errors

    new_id = max([int(user["id"]) for user in users], default=0) + 1

    users.append({
        "id": str(new_id),
        "email": new_email,
        "password": new_password,
        "role": new_role
    })
    return []


#Owner Role:
def Add_new_product():
    pass

def Update_prices():
    pass

def Restock_Inv():
    pass

def del_discontinued_items():
    pass

#Employee Role:

def current_cat():
    pass

def inv():
    pass

def daily_sales():
    pass

def ded_inv():
    pass
