import uuid
from typing import Optional, List, Dict

def current_cat(inventory: List[Dict], search: str) -> List[Dict]:
    if search:
        return [item for item in inventory if search.lower() in item["name"].lower()]
    return inventory

def inv(inventory: List[Dict], threshold: int = 10) -> List[Dict]:
    return [item for item in inventory if item["stock"] < threshold]

def daily_sales():
    pass

def ded_inv():
    pass
