from collections import OrderedDict


class TrieNode:
    def __init__(self):
        self.children: dict[str, "TrieNode"] = {}
        self.is_end: bool = False
        self.frequency: int = 0


class AutocompleteSystem:
    """Autocomplete system with LRU eviction and frequency tracking.

    Requirements addressed:
    * put(key,value) and get(key) operations
    * Fixed capacity with eviction of least-recently-used
    * Insert words with frequency, real-time updates
    * Return top-k suggestions for a prefix
    """

    def __init__(self, capacity: int = 1000):
        self.root = TrieNode()
        self.capacity = capacity
        # word -> frequency, recency tracked by order (last item is MRU)
        self.cache: OrderedDict[str, int] = OrderedDict()

    # ---------------- public cache methods ----------------
    def put(self, word: str, frequency: int = 1) -> None:
        """Insert/upsert a word with a given frequency.

        Updates recency; if capacity exceeded, evicts oldest entry.
        """
        if word in self.cache:
            # update frequency and move to end
            self.cache.move_to_end(word)
        else:
            if len(self.cache) >= self.capacity:
                old_word, _ = self.cache.popitem(last=False)
                self._delete_from_trie(old_word)
        self.cache[word] = frequency
        self._insert_in_trie(word, frequency)

    def get(self, word: str) -> int | None:
        """Retrieve a word frequency and bump its recency.

        Returns None when word not present.
        """
        if word in self.cache:
            self.cache.move_to_end(word)
            return self.cache[word]
        return None

    # ---------------- trie helpers ----------------
    def _insert_in_trie(self, word: str, frequency: int) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        node.frequency = frequency

    def _delete_from_trie(self, word: str) -> None:
        def _helper(node: TrieNode, index: int) -> bool:
            if index == len(word):
                if not node.is_end:
                    return False
                node.is_end = False
                node.frequency = 0
                return len(node.children) == 0
            char = word[index]
            child = node.children.get(char)
            if child is None:
                return False
            should_prune = _helper(child, index + 1)
            if should_prune:
                del node.children[char]
                return (not node.is_end) and len(node.children) == 0
            return False
        _helper(self.root, 0)

    def _find_node(self, prefix: str) -> TrieNode | None:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def _collect_words(self, node: TrieNode, prefix: str, results: list) -> None:
        if node.is_end:
            results.append((prefix, node.frequency))
        for char, child in node.children.items():
            self._collect_words(child, prefix + char, results)

    # ---------------- autocomplete ----------------
    def autocomplete(self, prefix: str, top_k: int = 5) -> list[str]:
        node = self._find_node(prefix)
        if not node:
            return []
        results: list[tuple[str, int]] = []
        self._collect_words(node, prefix, results)
        results.sort(key=lambda x: (-x[1], x[0]))
        return [word for word, _ in results[:top_k]]


if __name__ == "__main__":
    # demonstration of features
    sys = AutocompleteSystem(capacity=4)
    sys.put("apple", 5)
    sys.put("application", 3)
    sys.put("apply", 2)
    sys.put("app", 10)
    print("Suggestions for 'app'", sys.autocomplete("app", 3))
    sys.get("apple")
    sys.put("banana", 4)  # should evict least-recently-used (application)
    print("Cache contents", list(sys.cache.keys()))
    print("Suggestions for 'ban'", sys.autocomplete("ban"))
