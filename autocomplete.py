from typing import Dict, List, Tuple
import heapq


class TrieNode:
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}
        self.is_word: bool = False
        self.frequency: int = 0  # Only valid if is_word == True


class AutocompleteSystem:
    """Autocomplete data structure supporting insertion with frequency,
    real-time updates, and retrieving top-k suggestions for a given prefix.

    Uses a simple Trie. For each suggestion query, it performs a DFS over
    the subtree rooted at the prefix node collecting candidates in a heap.
    This approach is easy to reason about and supports updates immediately.
    """

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str, frequency: int = 1) -> None:
        """Insert a word with a given frequency. If the word already exists,
        its frequency is updated (increased by `frequency`)."""
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_word = True
        node.frequency += frequency

    def update(self, word: str, frequency: int) -> None:
        """Explicitly set the frequency of a word. Raises KeyError if the word
        doesn't exist."""
        node = self.root
        for ch in word:
            if ch not in node.children:
                raise KeyError(f"Word '{word}' not found")
            node = node.children[ch]
        if not node.is_word:
            raise KeyError(f"Word '{word}' not found")
        node.frequency = frequency

    def _find_prefix_node(self, prefix: str) -> TrieNode:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def _gather_words(self, node: TrieNode, prefix: str, heap: List[Tuple[int, str]], k: int):
        """Perform DFS from node and push (frequency, word) onto a min-heap
        that keeps at most k entries. The smallest frequency sits at root so that
        when the heap exceeds size k, the least frequent suggestion is removed.
        """
        if node.is_word:
            heapq.heappush(heap, (node.frequency, prefix))
            if len(heap) > k:
                heapq.heappop(heap)
        for ch, child in node.children.items():
            self._gather_words(child, prefix + ch, heap, k)

    def top_k(self, prefix: str, k: int) -> List[Tuple[str, int]]:
        """Return the top-k suggestions for a prefix, sorted by descending
        frequency. Each suggestion is a tuple (word, frequency)."""
        node = self._find_prefix_node(prefix)
        if node is None:
            return []
        heap: List[Tuple[int, str]] = []  # will store (freq, word) as a min-heap of top k
        self._gather_words(node, prefix, heap, k)
        # convert heap into sorted list (ascending by freq)
        result: List[Tuple[str, int]] = []
        while heap:
            freq, word = heapq.heappop(heap)
            result.append((word, freq))
        result.reverse()  # highest freq first
        return result


if __name__ == "__main__":
    # simple command line demo
    ac = AutocompleteSystem()
    ac.insert("apple", 5)
    ac.insert("app", 3)
    ac.insert("application", 2)
    ac.insert("banana", 4)

    print(ac.top_k("app", 3))
