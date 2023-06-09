import pickle

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        current = self.root
        for char in word:
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        current.is_end_of_word = True

    def search(self, word):
        current = self.root
        for char in word:
            if char not in current.children:
                return False
            current = current.children[char]
        return current.is_end_of_word

    def starts_with(self, prefix):
        current = self.root
        for char in prefix:
            if char not in current.children:
                return False
            current = current.children[char]
        return True

    def serialize(self):
        def serialize_helper(node):
            if not node:
                return ""
            serialized = []
            for char, child in node.children.items():
                serialized.append(char + serialize_helper(child))
            return "(" + "".join(serialized) + ")"

        return serialize_helper(self.root)

    @staticmethod
    def deserialize(serialized):
        def deserialize_helper(s, index):
            node = TrieNode()
            while index < len(s) and s[index] != ')':
                char = s[index]
                child, index = deserialize_helper(s, index + 1)
                node.children[char] = child
            return node, index + 1

        return deserialize_helper(serialized, 0)[0]
    
# file = open("ids.txt", "r")

# ids = file.read().split()
# dic =  Trie()
# for i in ids:
#     dic.insert(i)


# with open("ids.pickle", "wb") as file:
#     pickle.dump(dic, file)


"""
serialized_trie = dic.serialize()

with open("ID-Trie.txt", "w") as file:
    file.write(serialized_trie)"""