# ============================================================
# cart.py  —  ShopFlow
# CONCEPT: Duplicate Detection using Math (Sum Formula)
#
# 1. CART: When you add the same product twice, we detect it
#    and update quantity instead of adding a duplicate row.
#
# 2. DUPLICATE ORDER ID FINDER:
#    Given a list of IDs where exactly ONE is duplicated,
#    we find it using a math trick (no loops needed!):
#
#    Formula:
#      expected_sum = 0 + 1 + 2 + ... + (n-1) = n*(n-1)/2
#      actual_sum   = sum of all IDs given
#      duplicate    = actual_sum - expected_sum
#
#    Example: IDs = [0,1,2,3,2]  → n=5
#      expected = 4*5/2 = 10
#      actual   = 0+1+2+3+2 = 8    ← wait, that's wrong direction
#      Actually: expected = 0+1+2+3+4 = 10, actual = 8? No...
#
#    Corrected example: IDs = [1,2,3,2,4]  → n=5
#      expected = (n-1)*n/2 = 4*5/2 = 10
#      actual   = 1+2+3+2+4 = 12
#      duplicate = 12 - 10 = 2  ✓
# ============================================================


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

    def find_duplicate_id(self, id_list):
        """
        Math trick to find the one duplicate in a list of IDs.

        Assumes IDs are consecutive starting from 1 (or 0),
        with exactly one duplicate.

        Steps:
          1. n = total count of IDs
          2. expected_sum = sum of 1..n-1  (what sum SHOULD be with no duplicate)
          3. actual_sum = sum of IDs given
          4. duplicate = actual_sum - expected_sum
        """
        n = len(id_list)
        expected_sum = (n - 1) * n // 2   # sum of 0 to n-1
        actual_sum = sum(id_list)
        duplicate = actual_sum - expected_sum
        return duplicate
