import uuid
from typing import Optional, List, Dict
from datetime import date

#Filters the inventory based on a search term and returns matching items
def current_cat(inventory: List[Dict], search: str) -> List[Dict]:
    viewing_inventory = []
    if search:
        for item in inventory:
            if search.lower() in item["name"].lower():
                viewing_inventory.append(item)
            else:
                viewing_inventory = inventory

#Filters the inventory to return items that are low in stock based on a specified threshold
def inv(inventory: List[Dict], threshold: int = 10) -> List[Dict]:
    low_stock_items = []
    for item in inventory:
        if item.get("stock", 0) <= threshold:
            low_stock_items.append(item)
    return low_stock_items

#Processes daily sales data to return sales for the current day
def daily_sales(sales_data: List[Dict]) -> List[Dict]:
    today = date.today().isoformat()
    return [sale for sale in sales_data if sale.get("date") == today]


# Deducts sold items from the inventory
def ded_inv(inventory: List[Dict], sold_items: List[Dict]) -> List[Dict]:
    for sold_item in sold_items:
        for item in inventory:
            if item.get("id") == sold_item.get("id"):
                if item.get("stock", 0) >= sold_item.get("quantity", 0):
                    item["stock"] -= sold_item["quantity"]
                else:
                    item["stock"] = 0  # Set stock to 0 if sold quantity exceeds available stock
                break
    return inventory