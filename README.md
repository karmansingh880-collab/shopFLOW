# 🛒 ShopFLOW

ShopFLOW is a Python-based e-commerce simulation project that demonstrates the practical implementation of Data Structures, Algorithms, and Object-Oriented Programming concepts through a real-world shopping system.

The project provides product management, shopping cart operations, recently viewed products tracking, duplicate order detection, and delivery route optimization through an interactive Gradio web interface.

---

## 🚀 Features

### Product Catalog

* Browse available products.
* Demonstrates OOP concepts such as inheritance and polymorphism.
* Different product categories provide category-specific information.

### Recently Viewed Products

* Tracks recently viewed products.
* Implements an LRU (Least Recently Used) Cache using OrderedDict.
* Automatically removes the oldest item when cache capacity is exceeded.

### Shopping Cart

* Add and remove products.
* Updates quantity for duplicate products instead of creating multiple entries.
* Calculates total cart value dynamically.

### Duplicate Order ID Detection

* Detects duplicate IDs efficiently.
* Uses mathematical sum-based optimization.
* Demonstrates O(n) time complexity with O(1) extra space.

### Delivery Route Finder

* Models a delivery network using Graphs.
* Uses Breadth First Search (BFS) to determine shortest delivery routes.
* Simulates real-world logistics systems.

---

## 🛠️ Technologies Used

* Python
* Gradio
* Object-Oriented Programming (OOP)
* Graphs
* Breadth First Search (BFS)
* LRU Cache
* OrderedDict
* Data Structures & Algorithms

---

## 📂 Project Structure

```text
shopFLOW/
│
├── app.py               # Gradio UI
├── app_logic.py         # Application Logic
├── products.py          # Product Management & Polymorphism
├── cart.py              # Shopping Cart Operations
├── cache.py             # LRU Cache Implementation
├── delivery.py          # Graph & BFS Routing
├── requirements.txt     # Dependencies
└── HOW_IT_WORKS.md      # Detailed Documentation
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/karmansingh880-collab/shopFLOW.git
cd shopFLOW
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Open your browser and visit:

```text
http://localhost:7860
```

---

## 🎯 DSA Concepts Demonstrated

| Feature                  | Concept                        |
| ------------------------ | ------------------------------ |
| Product System           | OOP, Inheritance, Polymorphism |
| Recently Viewed Products | LRU Cache                      |
| Shopping Cart            | Hashing & Duplicate Handling   |
| Duplicate Finder         | Mathematical Optimization      |
| Delivery Routing         | Graphs                         |
| Route Search             | BFS Traversal                  |

---

## 📈 Learning Outcomes

* Applied Object-Oriented Programming principles.
* Implemented Graph traversal algorithms.
* Built an LRU Cache from scratch.
* Connected multiple DSA concepts into a single application.
* Developed a complete interactive web application using Gradio.

---

## 🔮 Future Enhancements

* User Authentication
* Database Integration
* Order History Tracking
* Payment Gateway Simulation
* Recommendation System
* Inventory Analytics Dashboard

---

## 👨‍💻 Author

Karman Singh

GitHub:
https://github.com/karmansingh880-collab
