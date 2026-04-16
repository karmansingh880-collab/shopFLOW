# ============================================================
# cache.py  —  ShopFlow
# CONCEPT: LRU Cache (Least Recently Used)
#
# When you browse products, we remember the last 3 you viewed.
# If you view a 4th new product, the OLDEST one is forgotten.
# If you re-view a product, it moves to the TOP (most recent).
#
# HOW: We use Python's OrderedDict.
#   - It keeps keys in insertion order.
#   - We treat the END = most recent, START = oldest.
#   - move_to_end()  → marks as recently used
#   - popitem(last=False) → removes the oldest item
# ============================================================

from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity=3):
        self.capacity = capacity          # max number of items to remember
        self.cache = OrderedDict()        # {product_id: product_name}

    def view_product(self, product):
        """
        Record that the user viewed this product.
        Returns a message describing what happened.
        """
        pid = product.product_id
        messages = []

        if pid in self.cache:
            # Already viewed before → just move it to top (most recent)
            self.cache.move_to_end(pid)
            messages.append(f"🔄 '{product.name}' moved to top (viewed again).")
        else:
            if len(self.cache) >= self.capacity:
                # Cache is full → remove the oldest item first
                removed_id, removed_name = self.cache.popitem(last=False)
                messages.append(f"🗑️ Cache full — removed '{removed_name}' (oldest).")

            # Add the new product at the end (most recent position)
            self.cache[pid] = product.name
            messages.append(f"👁️ Now viewing: '{product.name}'")

        return messages

    def get_recently_viewed(self):
        """
        Return recently viewed products, newest first.
        Returns a list of (rank, name, product_id) tuples.
        """
        # Reverse the list so index 1 = most recent
        items = list(self.cache.items())[::-1]
        return [(i + 1, name, pid) for i, (pid, name) in enumerate(items)]

    def clear(self):
        """Reset the cache."""
        self.cache.clear()
