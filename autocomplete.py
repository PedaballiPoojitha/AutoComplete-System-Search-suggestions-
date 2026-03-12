class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.frequency = 0

class AutocompleteSystem:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word, frequency=1):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        node.frequency += frequency
    
    def _find_node(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
    
    def _collect_words(self, node, prefix, results):
        if node.is_end:
            results.append((prefix, node.frequency))
        for char, child in node.children.items():
            self._collect_words(child, prefix + char, results)
    
    def autocomplete(self, prefix, top_k=5):
        node = self._find_node(prefix)
        if not node:
            return []
        results = []
        self._collect_words(node, prefix, results)
        results.sort(key=lambda x: (-x[1], x[0]))
        return [word for word, _ in results[:top_k]]

if __name__ == "__main__":
    system = AutocompleteSystem()
    words = ["apple", "application", "apply", "app", "banana", "band"]
    for word in words:
        system.insert(word)
    
    print("Autocomplete 'app':", system.autocomplete("app"))
    print("Autocomplete 'ban':", system.autocomplete("ban"))
