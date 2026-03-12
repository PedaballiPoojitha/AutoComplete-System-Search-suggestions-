import heapq

class TrieNode:
    def __init__(self):
        self.children = {}
        self.freq = 0
        self.is_end = False

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
        node.freq += frequency
    
    def _dfs(self, node, prefix, results):
        if node.is_end:
            results.append((node.freq, prefix))
        for char, child in node.children.items():
            self._dfs(child, prefix + char, results)
    
    def search(self, prefix, k=5):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        
        results = []
        self._dfs(node, prefix, results)
        return [word for _, word in heapq.nlargest(k, results)]

if __name__ == "__main__":
    print("\n=== AUTOCOMPLETE SYSTEM ===")
    ac = AutocompleteSystem()
    
    # Pre-load some words
    ac.insert("apple", 5)
    ac.insert("app", 3)
    ac.insert("application", 2)
    ac.insert("apply", 4)
    ac.insert("appreciate", 3)
    
    while True:
        print("\n" + "="*40)
        print("1. Add Word")
        print("2. Search")
        print("3. Exit")
        choice = input("Enter choice: ")
        
        if choice == '1':
            word = input("Enter word: ")
            freq = int(input("Enter frequency (default 1): ") or "1")
            ac.insert(word, freq)
            print(f"✓ Added '{word}' with frequency {freq}")
        elif choice == '2':
            prefix = input("Enter search prefix: ")
            k = int(input("How many suggestions? ") or "5")
            results = ac.search(prefix, k)
            if results:
                print(f"\nSuggestions: {results}")
            else:
                print("No suggestions found")
        elif choice == '3':
            break
