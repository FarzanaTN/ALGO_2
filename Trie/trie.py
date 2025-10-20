class Node:
    def __init__(self):
        self.children = [None] * 26
        self.eow = False  # end of word


root = Node()

def insert(word):
    global root
    node = root  # keep reference so root isn't lost
    for i in range(len(word)):
        idx = ord(word[i]) - ord('a')
        if node.children[idx] is None:
            node.children[idx] = Node()
        if i == len(word) - 1:
            node.children[idx].eow = True
        node = node.children[idx]


def search(key):
    global root
    node = root
    for i in range(len(key)):
        idx = ord(key[i]) - ord('a')
        if node.children[idx] is None:
            return False
        node = node.children[idx]
        if i == len(key) - 1 and not node.eow:
            return False
    return True


# Example usage
insert("apple")
insert("app")

print(search("app"))    # True
print(search("apple"))  # True
print(search("appl"))   # False
