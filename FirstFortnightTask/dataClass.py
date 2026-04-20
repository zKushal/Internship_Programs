from dataclasses import dataclass


@dataclass
class InventoryItem:
    name: str
    price: float
    quantity: int

item1 = InventoryItem("Widget", 19.99, 100)
print(item1)