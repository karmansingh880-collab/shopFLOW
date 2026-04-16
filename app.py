# ============================================================
# app.py  —  ShopFlow Gradio UI
#
# HOW TO RUN:
#   pip install gradio
#   python app.py
#   Then open http://localhost:7860 in your browser
#
# STRUCTURE:
#   We use gr.Tabs() to create 5 tabs, one per feature:
#   1. 🛍️  Catalog         — view all products
#   2. 👁️  Recently Viewed — LRU Cache demo
#   3. 🛒  Cart            — add/remove items, checkout
#   4. 🔍  Duplicate Finder — math trick for duplicate IDs
#   5. 🚚  Delivery Route  — BFS shortest path finder
# ============================================================

import gradio as gr
from app_logic import (
    get_catalog_display,
    view_product,
    add_to_cart,
    get_cart_display,
    remove_from_cart,
    checkout,
    find_duplicate,
    find_route,
)

# ── Shared column headers ─────────────────────────────────────
CATALOG_HEADERS  = ["ID", "Name", "Price", "Category", "Extra Info"]
CART_HEADERS     = ["Product", "Unit Price", "Qty", "Subtotal"]
LRU_HEADERS      = ["Rank", "Product Name", "Product ID"]
NETWORK_HEADERS  = ["City", "Connected To"]

# ── CSS for a clean look ──────────────────────────────────────
CSS = """
#title    { text-align: center; color: #4f46e5; font-size: 2em; font-weight: bold; }
#subtitle { text-align: center; color: #6b7280; margin-bottom: 1em; }
.tab-nav  { font-size: 1.05em !important; }
footer    { display: none !important; }
"""

# ── Build the Gradio App ──────────────────────────────────────
with gr.Blocks(css=CSS, title="ShopFlow") as app:

    # ── Header ────────────────────────────────────────────────
    gr.Markdown("# 🛒 ShopFlow", elem_id="title")
    gr.Markdown("Simple E-commerce Mini Project — DSA Concepts in Action", elem_id="subtitle")

    with gr.Tabs(elem_classes="tab-nav"):

        # ════════════════════════════════════════════════════
        # TAB 1 — Product Catalog
        # ════════════════════════════════════════════════════
        with gr.Tab("🛍️ Catalog"):
            gr.Markdown("### All Available Products")
            gr.Markdown(
                "**Concept used: Polymorphism** — Each product type (Electronics, Clothing, Food) "
                "has its own `display()` method. Python calls the right one automatically."
            )
            catalog_btn = gr.Button("🔄 Load / Refresh Catalog", variant="primary")
            catalog_table = gr.Dataframe(
                headers=CATALOG_HEADERS,
                datatype=["number", "str", "str", "str", "str"],
                interactive=False,
                label="Product Catalog",
            )
            catalog_btn.click(fn=get_catalog_display, outputs=catalog_table)

        # ════════════════════════════════════════════════════
        # TAB 2 — Recently Viewed (LRU Cache)
        # ════════════════════════════════════════════════════
        with gr.Tab("👁️ Recently Viewed"):
            gr.Markdown("### Recently Viewed Products — LRU Cache")
            gr.Markdown(
                "**Concept used: LRU Cache (OrderedDict)** — Remembers the last 3 products you viewed. "
                "If you view a 4th new product, the oldest is removed. Re-viewing a product moves it to top."
            )
            with gr.Row():
                lru_id_input = gr.Textbox(label="Enter Product ID", placeholder="e.g. 101", scale=3)
                lru_btn = gr.Button("👁️ View Product", variant="primary", scale=1)
            lru_log   = gr.Textbox(label="Cache Log", lines=3, interactive=False)
            lru_table = gr.Dataframe(headers=LRU_HEADERS, interactive=False, label="Recently Viewed (newest first)")
            lru_btn.click(fn=view_product, inputs=lru_id_input, outputs=[lru_log, lru_table])

        # ════════════════════════════════════════════════════
        # TAB 3 — Cart
        # ════════════════════════════════════════════════════
        with gr.Tab("🛒 Cart"):
            gr.Markdown("### Shopping Cart")
            gr.Markdown(
                "**Concept used: Duplicate Detection** — Adding the same product twice updates "
                "quantity instead of duplicating the row."
            )

            with gr.Row():
                cart_id_input  = gr.Textbox(label="Product ID",  placeholder="e.g. 201", scale=2)
                cart_qty_input = gr.Textbox(label="Quantity",     placeholder="e.g. 2",   scale=1)
                cart_add_btn   = gr.Button("➕ Add to Cart",  variant="primary", scale=1)

            with gr.Row():
                remove_id_input = gr.Textbox(label="Product ID to Remove", placeholder="e.g. 201", scale=3)
                cart_rem_btn    = gr.Button("🗑️ Remove Item", variant="secondary", scale=1)

            cart_msg     = gr.Textbox(label="Message", lines=2, interactive=False)
            cart_table   = gr.Dataframe(headers=CART_HEADERS, interactive=False, label="Cart Items")
            cart_total   = gr.Textbox(label="Total", interactive=False)

            with gr.Row():
                cart_view_btn = gr.Button("🔄 Refresh Cart",  scale=1)
                checkout_btn  = gr.Button("✅ Checkout",       variant="primary", scale=1)

            cart_add_btn.click(fn=add_to_cart,   inputs=[cart_id_input, cart_qty_input], outputs=[cart_msg, cart_table, cart_total])
            cart_rem_btn.click(fn=remove_from_cart, inputs=remove_id_input,              outputs=[cart_msg, cart_table, cart_total])
            cart_view_btn.click(fn=get_cart_display,                                     outputs=[cart_table, cart_total])
            checkout_btn.click(fn=checkout,                                              outputs=[cart_msg, cart_table])

        # ════════════════════════════════════════════════════
        # TAB 4 — Duplicate Order ID Finder
        # ════════════════════════════════════════════════════
        with gr.Tab("🔍 Duplicate Finder"):
            gr.Markdown("### Duplicate Order ID Detector")
            gr.Markdown(
                "**Concept used: Sum Formula (Exp 2)** — Given a list of consecutive IDs where "
                "exactly ONE is duplicated, we find it instantly using math: "
                "`duplicate = actual_sum − expected_sum`"
            )
            dup_input = gr.Textbox(
                label="Enter Order IDs (space-separated, one should be duplicate)",
                placeholder="e.g. 1 2 3 2 4",
            )
            dup_btn    = gr.Button("🔍 Find Duplicate", variant="primary")
            dup_output = gr.Textbox(label="Result", lines=5, interactive=False)
            dup_btn.click(fn=find_duplicate, inputs=dup_input, outputs=dup_output)

        # ════════════════════════════════════════════════════
        # TAB 5 — Delivery Route
        # ════════════════════════════════════════════════════
        with gr.Tab("🚚 Delivery Route"):
            gr.Markdown("### Delivery Route Finder — BFS on a Graph")
            gr.Markdown(
                "**Concept used: Graph + BFS** — Cities are nodes, roads are edges. "
                "BFS guarantees the **shortest path** (fewest hops) from Warehouse to your city."
            )
            with gr.Row():
                city_input  = gr.Dropdown(
                    choices=["Mohali", "Chandigarh", "Panchkula", "Ambala"],
                    label="Select your city",
                    scale=3,
                )
                route_btn   = gr.Button("🚚 Find Route", variant="primary", scale=1)
            route_output = gr.Textbox(label="Route Result", lines=4, interactive=False)
            net_table    = gr.Dataframe(headers=NETWORK_HEADERS, interactive=False, label="Delivery Network Map")
            route_btn.click(fn=find_route, inputs=city_input, outputs=[route_output, net_table])

    # ── Footer info ───────────────────────────────────────────
    gr.Markdown(
        "---\n"
        "**ShopFlow** | Concepts: Polymorphism • LRU Cache • Duplicate Detection • BFS Graph Traversal"
    )

# ── Launch ────────────────────────────────────────────────────
if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",   # accessible on local network
        server_port=7860,
        share=False,             # set True to get a public link
        inbrowser=True,          # auto-open browser
    )
