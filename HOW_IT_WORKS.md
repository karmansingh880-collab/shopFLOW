# 📘 ShopFlow — How It Works
> A complete explanation of every file, every concept, and how they connect.

---

## 🗂️ Project Structure

```
shopflow/
│
├── products.py      ← OOP + Polymorphism
├── cache.py         ← LRU Cache (OrderedDict)
├── cart.py          ← Duplicate Detection (Sum Formula)
├── delivery.py      ← Graph + BFS Traversal
│
├── app_logic.py     ← Connects all modules; functions for the UI
├── app.py           ← Gradio UI (runs the web interface)
│
└── HOW_IT_WORKS.md  ← You're reading this!
```

---

## 🚀 How to Run

```bash
pip install gradio
python app.py
# Open http://localhost:7860 in your browser
```

---

## 📦 File-by-File Explanation

---

### 1. `products.py` — Polymorphism (OOP)

**Concept:** Polymorphism means "many forms." One method name, different behaviour.

**How it works:**
- `Product` is the **base class** with `get_category()` and `get_extra_info()` methods.
- `Electronics`, `Clothing`, `Food` are **child classes** that override these methods.
- When we call `product.get_extra_info()`, Python automatically uses the right version.

```python
# Base class
class Product:
    def get_extra_info(self):
        return ""

# Child class — overrides the method
class Electronics(Product):
    def get_extra_info(self):
        return "Warranty: 1 Year"

# Python calls the RIGHT method automatically:
p = Electronics(101, "Headphones", 1500)
print(p.get_extra_info())  # → "Warranty: 1 Year"
```

**Real-world use:** Product pages on Amazon, Flipkart — each product type shows different info.

---

### 2. `cache.py` — LRU Cache (Least Recently Used)

**Concept:** An LRU Cache keeps track of the last N items used. When it's full, it drops the OLDEST one.

**Data Structure Used:** Python's `OrderedDict`
- Maintains insertion order
- `move_to_end(key)` → marks as recently used
- `popitem(last=False)` → removes the oldest (first) item

**How it works step by step:**

```
Capacity = 3

View 101 → Cache: [101]
View 102 → Cache: [101, 102]
View 201 → Cache: [101, 102, 201]
View 202 → Cache full! Drop 101 (oldest)
           Cache: [102, 201, 202]
View 102 → Already there! Move to top
           Cache: [201, 202, 102]
```

```python
cache = OrderedDict()

# View product 101
cache[101] = "Headphones"

# Re-view 101 → move to end (most recent)
cache.move_to_end(101)

# Cache full → remove first (oldest)
cache.popitem(last=False)
```

**Real-world use:** Browser history, YouTube watch history, CPU memory caching.

---

### 3. `cart.py` — Duplicate Detection (Math Trick)

**Concept A — Cart Duplicate Detection:**
When you add a product that's already in the cart, we update quantity instead of adding a second row.

```python
for item in self.items:
    if item["id"] == product.product_id:
        item["quantity"] += quantity   # update, not duplicate
        return
```

**Concept B — Duplicate Order ID (Sum Formula):**
Given a list of IDs where one is duplicated:

```
Formula:
  expected_sum = 0 + 1 + 2 + ... + (n-1) = n*(n-1)/2
  actual_sum   = sum of all IDs given
  duplicate    = actual_sum - expected_sum

Example: [1, 2, 3, 2, 4]  →  n = 5
  expected = 4*5/2 = 10
  actual   = 1+2+3+2+4 = 12
  duplicate = 12 - 10 = 2  ✓
```

**Why this is clever:** No nested loops. O(n) time, O(1) space. Pure math!

**Real-world use:** Detecting duplicate transactions in payment systems.

---

### 4. `delivery.py` — Graph + BFS Traversal

**Concept:** A graph is a network of nodes (cities) connected by edges (roads).

**BFS (Breadth-First Search):**
Explores all neighbours at distance 1 first, then distance 2, etc.
This guarantees the SHORTEST path (fewest hops).

**Delivery network:**
```
Warehouse ──── Mohali ──── Panchkula ──── Ambala
     └────── Chandigarh ──┘
```

**BFS Step-by-step (Warehouse → Ambala):**
```
Queue: [(Warehouse, [Warehouse])]

Step 1: Visit Warehouse → neighbours: Mohali, Chandigarh
        Queue: [(Mohali, [W,M]), (Chandigarh, [W,C])]

Step 2: Visit Mohali → neighbours: Panchkula
        Queue: [(Chandigarh, [W,C]), (Panchkula, [W,M,P])]

Step 3: Visit Chandigarh → Panchkula (already queued)
        Queue: [(Panchkula, [W,M,P])]

Step 4: Visit Panchkula → neighbours: Ambala
        Queue: [(Ambala, [W,M,P,A])]

Step 5: Visit Ambala = DESTINATION!
        Return: Warehouse → Mohali → Panchkula → Ambala
```

**Real-world use:** Google Maps route finding, network packet routing.

---

### 5. `app_logic.py` — The Bridge

This file:
- Creates ONE shared `Cart`, `LRUCache`, `DeliveryGraph` for the whole app
- Wraps all business logic into simple functions
- Returns data as lists/strings that Gradio can display
- Keeps `app.py` clean (only UI code there)

---

### 6. `app.py` — The Gradio UI

**What is Gradio?**
A Python library to build web UIs with just a few lines of code. No HTML/CSS needed.

**Key Gradio components used:**

| Component | Purpose |
|-----------|---------|
| `gr.Blocks()` | Full layout control |
| `gr.Tabs()` | Multiple tabs |
| `gr.Textbox()` | Text input/output |
| `gr.Dataframe()` | Display tables |
| `gr.Button()` | Clickable button |
| `gr.Dropdown()` | Select from list |

**How a button works:**
```python
btn.click(
    fn=my_function,        # function to call
    inputs=[input1, ...],  # read values from these
    outputs=[output1, ...]  # write results to these
)
```

---

## 🔗 How Everything Connects

```
app.py  (UI layer)
   │
   ├── calls app_logic.py  (business logic layer)
   │       │
   │       ├── products.py  → get_catalog(), find_product_by_id()
   │       ├── cache.py     → LRUCache.view_product()
   │       ├── cart.py      → Cart.add_item(), find_duplicate_id()
   │       └── delivery.py  → DeliveryGraph.bfs_route()
   │
   └── displays results in Gradio widgets
```

---

## 🧠 DSA Concepts Summary

| Feature | Module | DSA Concept |
|---------|--------|-------------|
| Product types | products.py | Polymorphism (OOP) |
| Recently Viewed | cache.py | LRU Cache (OrderedDict) |
| Cart duplicates | cart.py | Linear search |
| Duplicate ID finder | cart.py | Math sum formula O(n) |
| Delivery route | delivery.py | Graph + BFS |

---

*ShopFlow — Built to demonstrate Data Structures & Algorithms through a real-world mini project.*
