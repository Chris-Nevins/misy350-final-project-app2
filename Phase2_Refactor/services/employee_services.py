import uuid
from typing import List, Dict
from datetime import date

# 1) Filter inventory by search term
def current_cat(inventory: List[Dict], search: str) -> List[Dict]:
    if not search:
        return inventory

    search = search.lower()
    return [
        item for item in inventory
        if search in item.get("name", "").lower()
    ]


# 2) Get low stock items
def inv(inventory: List[Dict], threshold: int = 10) -> List[Dict]:
    return [
        item for item in inventory
        if item.get("stock", 0) <= threshold
    ]


# 3) Get today's sales only
def daily_sales(sales_data: List[Dict]) -> List[Dict]:
    today = date.today().isoformat()
    return [
        sale for sale in sales_data
        if sale.get("date") == today
    ]


# 4) Deduct sold quantities from inventory
def ded_inv(inventory: List[Dict], sold_items: List[Dict]) -> List[Dict]:
    inv_map = {item["id"]: item for item in inventory}

    for sold in sold_items:
        item_id = sold.get("id")
        qty = sold.get("quantity", 0)

        if item_id in inv_map:
            inv_map[item_id]["stock"] = max(
                0,
                inv_map[item_id].get("stock", 0) - qty
            )

    return list(inv_map.values())