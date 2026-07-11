# ============================================================
# cart.py  —  ShopFlow
# CONCEPT: Duplicate Detection using SQL
#
# 1. CART: When you add the same product twice, we detect it
#    and update quantity instead of adding a duplicate row.
#
# 2. DUPLICATE ORDER ID FINDER (SQL):
#    We insert all the entered IDs into a tiny temporary SQLite
#    table and ask the database itself to find the duplicate:
#
#      SELECT order_id, COUNT(*) FROM orders
#      GROUP BY order_id
#      HAVING COUNT(*) > 1;
#
#    This is how you'd realistically find duplicates in a real
#    database full of orders — SQL does the counting for us.
# ============================================================

import sqlite3


class Cart:
    def __init__(self):
        self.items = []   # list of dicts: {id, name, price, quantity}

    def add_item(self, product, quantity=1):
        """
        Add a product to the cart.
        If it's already there, just increase the quantity.
        Returns a message about what happened.
        """
        # Check if this product is already in the cart
        for item in self.items:
            if item["id"] == product.product_id:
                item["quantity"] += quantity
                return f"🔄 '{product.name}' already in cart — quantity updated to {item['quantity']}."

        # New product — add it fresh
        self.items.append({
            "id":       product.product_id,
            "name":     product.name,
            "price":    product.price,
            "quantity": quantity,
        })
        return f"✅ '{product.name}' added to cart (qty: {quantity})."

    def remove_item(self, product_id):
        """Remove an item from the cart by product ID."""
        for i, item in enumerate(self.items):
            if item["id"] == product_id:
                name = item["name"]
                self.items.pop(i)
                return f"🗑️ '{name}' removed from cart."
        return "❌ Product not found in cart."

    def get_cart_rows(self):
        """Return cart items as a list of dicts (for UI display)."""
        rows = []
        for item in self.items:
            rows.append({
                "name":     item["name"],
                "price":    item["price"],
                "quantity": item["quantity"],
                "subtotal": item["price"] * item["quantity"],
            })
        return rows

    def get_total(self):
        """Calculate total price of all items in cart."""
        return sum(item["price"] * item["quantity"] for item in self.items)

    def clear(self):
        """Empty the cart."""
        self.items.clear()

    def find_duplicate_id_sql(self, id_list):
        """
        SQL version of the same duplicate finder.

        Uses an in-memory SQLite database (created fresh each
        call, thrown away after — no file is saved to disk).

        Steps:
          1. Create a temporary 'orders' table.
          2. Insert every ID from id_list as a row.
          3. Run GROUP BY + HAVING COUNT(*) > 1 to find any ID
             that appears more than once.
          4. Return the duplicate ID (or None if none found).
        """
        conn = sqlite3.connect(":memory:")   # temporary DB, lives only in RAM
        conn.execute("CREATE TABLE orders (order_id INTEGER)")
        conn.executemany(
            "INSERT INTO orders (order_id) VALUES (?)",
            [(i,) for i in id_list],
        )

        cursor = conn.execute(
            "SELECT order_id, COUNT(*) as times "
            "FROM orders "
            "GROUP BY order_id "
            "HAVING COUNT(*) > 1"
        )
        result = cursor.fetchone()   # (order_id, times) or None
        conn.close()

        return result[0] if result else None
