# ============================================================
# app_logic.py  —  ShopFlow
# This file holds the SHARED STATE for the Gradio app.
#
# Why a separate file?
#   Gradio can call our functions from many tabs.
#   We need ONE shared cart, ONE shared cache, and ONE shared
#   delivery network — not a new one per button click.
#
# All the Gradio button functions live here, calling the
# clean logic in products.py, cart.py, cache.py, delivery.py.
# ============================================================

from products import get_catalog, find_product_by_id, get_catalog_as_dicts
from cart import Cart
from cache import LRUCache
from delivery import setup_delivery_network

# ── Global shared state ──────────────────────────────────────
# These are created ONCE when the app starts.
cart           = Cart()
recently_viewed = LRUCache(capacity=3)
delivery        = setup_delivery_network()
catalog         = get_catalog()


# ── Helper ───────────────────────────────────────────────────

def _catalog_table():
    """Return catalog formatted as a list of lists for gr.Dataframe."""
    rows = []
    for p in catalog:
        d = p.to_dict()
        rows.append([d["id"], d["name"], f"Rs. {d['price']}", d["category"], d["extra"]])
    return rows


# ── Feature 1: View Catalog ──────────────────────────────────

def get_catalog_display():
    return _catalog_table()


# ── Feature 2: View Product (LRU Cache) ──────────────────────

def view_product(product_id_str):
    """Called when user clicks 'View Product' in the LRU tab."""
    try:
        pid = int(product_id_str)
    except ValueError:
        return "❌ Please enter a valid number.", []

    product = find_product_by_id(pid)
    if not product:
        return f"❌ Product ID {pid} not found.", []

    messages = recently_viewed.view_product(product)
    log = "\n".join(messages)

    # Build recently viewed table
    rv = recently_viewed.get_recently_viewed()
    table = [[rank, name, f"ID: {pid2}"] for rank, name, pid2 in rv]

    return log, table


# ── Feature 3: Add to Cart ───────────────────────────────────

def add_to_cart(product_id_str, quantity_str):
    """Called when user clicks 'Add to Cart'."""
    try:
        pid = int(product_id_str)
        qty = int(quantity_str)
        if qty < 1:
            return "❌ Quantity must be at least 1.", [], "Rs. 0"
    except ValueError:
        return "❌ Enter valid numbers.", [], "Rs. 0"

    product = find_product_by_id(pid)
    if not product:
        return f"❌ Product ID {pid} not found.", [], "Rs. 0"

    msg = cart.add_item(product, qty)
    return msg, _cart_table(), f"Rs. {cart.get_total()}"


def _cart_table():
    rows = []
    for item in cart.get_cart_rows():
        rows.append([item["name"], f"Rs. {item['price']}", item["quantity"], f"Rs. {item['subtotal']}"])
    return rows


def get_cart_display():
    return _cart_table(), f"Rs. {cart.get_total()}"


def remove_from_cart(product_id_str):
    try:
        pid = int(product_id_str)
    except ValueError:
        return "❌ Enter a valid product ID.", [], "Rs. 0"
    msg = cart.remove_item(pid)
    return msg, _cart_table(), f"Rs. {cart.get_total()}"


def checkout():
    total = cart.get_total()
    if total == 0:
        return "🛒 Cart is empty! Add some products first.", []
    summary = _cart_table()
    cart.clear()
    return f"🎉 Order placed! Total paid: Rs. {total}. Thank you!", summary


# ── Feature 4: Duplicate ID Finder ───────────────────────────

def find_duplicate(id_string):
    """Called when user clicks 'Find Duplicate'."""
    try:
        id_list = list(map(int, id_string.strip().split()))
    except ValueError:
        return "❌ Enter only numbers separated by spaces."

    if len(id_list) < 2:
        return "❌ Enter at least 2 numbers."

    dup = cart.find_duplicate_id(id_list)
    return (
        f"📋 IDs entered : {id_list}\n"
        f"🔍 Expected sum: {(len(id_list)-1)*len(id_list)//2}\n"
        f"➕ Actual sum  : {sum(id_list)}\n"
        f"✅ Duplicate ID: {dup}  ← this order was placed twice!"
    )


# ── Feature 5: Delivery Route ─────────────────────────────────

def find_route(destination):
    """Called when user clicks 'Find Route'."""
    destination = destination.strip()
    if not destination:
        return "❌ Please enter a city name.", []

    route = delivery.bfs_route("Warehouse", destination)

    if route:
        path_str = " → ".join(route)
        msg = f"✅ Route found!\n📍 {path_str}\n🏁 Total stops: {len(route)}"
    else:
        msg = f"❌ No route found to '{destination}'.\nAvailable cities: {', '.join(delivery.get_all_cities())}"

    # Network map table
    net = [[row["city"], row["connected_to"]] for row in delivery.get_network_info()]
    return msg, net
