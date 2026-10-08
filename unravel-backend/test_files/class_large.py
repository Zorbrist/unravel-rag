"""Sample module containing a single class with multiple methods."""


class InventoryManager:
    """Manages a simple in-memory inventory of products."""

    def __init__(self, name="Main Warehouse"):
        self.name = name
        self.items = {}
        self.history = []

    def add_item(self, sku, description, quantity=0, price=0.0):
        """Add a new item to the inventory."""
        if sku in self.items:
            raise ValueError(f"SKU {sku} already exists")
        self.items[sku] = {
            "description": description,
            "quantity": quantity,
            "price": price,
        }
        self.history.append(("add", sku, quantity))
        return self.items[sku]

    def remove_item(self, sku):
        """Remove an item entirely from the inventory."""
        if sku not in self.items:
            raise KeyError(f"SKU {sku} not found")
        removed = self.items.pop(sku)
        self.history.append(("remove", sku, removed["quantity"]))
        return removed

    def restock(self, sku, amount):
        """Increase the quantity of an existing item."""
        if amount <= 0:
            raise ValueError("Restock amount must be positive")
        self._require(sku)
        self.items[sku]["quantity"] += amount
        self.history.append(("restock", sku, amount))
        return self.items[sku]["quantity"]

    def sell(self, sku, amount):
        """Decrease quantity and return the total sale value."""
        self._require(sku)
        item = self.items[sku]
        if amount > item["quantity"]:
            raise ValueError("Insufficient stock")
        item["quantity"] -= amount
        self.history.append(("sell", sku, amount))
        return round(amount * item["price"], 2)

    def total_value(self):
        """Return the total value of all stock on hand."""
        return round(
            sum(i["quantity"] * i["price"] for i in self.items.values()), 2
        )

    def low_stock(self, threshold=5):
        """Return SKUs whose quantity is at or below the threshold."""
        return [
            sku for sku, i in self.items.items() if i["quantity"] <= threshold
        ]

    def search(self, keyword):
        """Find items whose description contains the keyword."""
        keyword = keyword.lower()
        return {
            sku: i
            for sku, i in self.items.items()
            if keyword in i["description"].lower()
        }

    def report(self):
        """Build a human-readable text report."""
        lines = [f"Inventory report: {self.name}", "-" * 40]
        for sku, i in sorted(self.items.items()):
            lines.append(
                f"{sku:<10} {i['description']:<20} "
                f"qty={i['quantity']:<4} ${i['price']:.2f}"
            )
        lines.append("-" * 40)
        lines.append(f"Total value: ${self.total_value():.2f}")
        return "\n".join(lines)

    def _require(self, sku):
        if sku not in self.items:
            raise KeyError(f"SKU {sku} not found")


if __name__ == "__main__":
    inv = InventoryManager()
    inv.add_item("A100", "Widget", 10, 2.50)
    inv.add_item("B200", "Gadget", 3, 12.00)
    inv.sell("A100", 4)
    inv.restock("B200", 5)
    print(inv.report())
    print("Low stock:", inv.low_stock())