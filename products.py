# ============================================================
# products.py  —  ShopFlow
# CONCEPT: Polymorphism (OOP)
#
# We have ONE base class (Product) and THREE child classes:
#   Electronics, Clothing, Food
#
# Each child has its own display() method.
# Python automatically calls the RIGHT display() depending on
# the object type — that's polymorphism!
# ============================================================


class Product:
    """Base class — every product has an ID, name, and price."""

    def __init__(self, product_id, name, price):
        self.product_id = product_id
        self.name = name
        self.price = price

    def get_category(self):
        return "General"

    def get_extra_info(self):
        return ""

    def to_dict(self):
        """Return product info as a dictionary (useful for the UI)."""
        return {
            "id": self.product_id,
            "name": self.name,
            "price": self.price,
            "category": self.get_category(),
            "extra": self.get_extra_info(),
        }


class Electronics(Product):
    """Child class for electronic items. Adds warranty info."""

    def get_category(self):
        return "Electronics"

    def get_extra_info(self):
        return "Warranty: 1 Year"


class Clothing(Product):
    """Child class for clothing items. Adds return policy info."""

    def get_category(self):
        return "Clothing"

    def get_extra_info(self):
        return "Return: Free within 7 days"


class Food(Product):
    """Child class for food items. Adds expiry info."""

    def get_category(self):
        return "Food"

    def get_extra_info(self):
        return "Expiry: Best before 7 days"


# ── Catalog ──────────────────────────────────────────────────

def get_catalog():
    """Returns the full list of products available in the shop."""
    return [
        Electronics(101, "Headphones",    1500),
        Electronics(102, "Keyboard",       800),
        Clothing   (201, "T-Shirt",        499),
        Clothing   (202, "Jacket",        1200),
        Food       (301, "Chocolate Box",  250),
        Food       (302, "Chips Pack",      50),
    ]


def get_catalog_as_dicts():
    """Returns catalog as a list of dicts — easy to use in the UI."""
    return [p.to_dict() for p in get_catalog()]


def find_product_by_id(product_id):
    """Search the catalog for a product by its ID. Returns None if not found."""
    for p in get_catalog():
        if p.product_id == product_id:
            return p
    return None
