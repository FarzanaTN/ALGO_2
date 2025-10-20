class Node:
    def __init__(self):
        self.children = {}
        self.eow = False
        self.indexes = []  # starting positions of suffixes


class CompNode:
    def __init__(self):
        self.children = {}   # edge_label (string) → CompNode
        self.eow = False
        self.indexes = []


def build_suffix_trie(s):
    """Build the full (uncompressed) suffix trie, case-insensitive."""
    s = s.lower()
    root = Node()
    for i in range(len(s)):
        node = root
        for ch in s[i:]:
            if ch not in node.children:
                node.children[ch] = Node()
            node = node.children[ch]
            node.indexes.append(i)
        node.eow = True
    return root


def compress(node):
    """Compress the trie into a compact edge-labeled form."""
    comp = CompNode()
    comp.eow = node.eow
    comp.indexes = node.indexes.copy()  # <-- keep index info

    for ch, child in node.children.items():
        label = ch
        curr = child
        # collapse single-child paths that are not end-of-word
        while len(curr.children) == 1 and not curr.eow:
            (next_ch, next_node), = curr.children.items()
            label += next_ch
            curr = next_node
        comp.children[label] = compress(curr)
    return comp


def search_positions(comp_root, pattern):
    """
    Return all starting indices where 'pattern' appears (case-insensitive).
    If pattern ends inside an edge label, it's still valid.
    """
    node = comp_root
    pattern = pattern.lower()
    i = 0
    while i < len(pattern):
        found = False
        for label, child in node.children.items():
            label_lower = label.lower()
            # Full label match
            if pattern.startswith(label_lower, i):
                i += len(label_lower)
                node = child
                found = True
                break
            # Pattern ends inside edge label
            elif label_lower.startswith(pattern[i:]):
                return child.indexes
        if not found:
            return []
    return node.indexes


def search_substring(comp_root, pattern):
    """Return True if pattern exists as a substring (case-insensitive)."""
    node = comp_root
    pattern = pattern.lower()
    i = 0
    while i < len(pattern):
        found = False
        for label, child in node.children.items():
            label_lower = label.lower()
            if pattern.startswith(label_lower, i):
                i += len(label_lower)
                node = child
                found = True
                break
            elif label_lower.startswith(pattern[i:]):
                return True
        if not found:
            return False
    return True


def search_is_suffix(comp_root, pattern):
    """Return True if pattern is a full suffix (case-insensitive)."""
    node = comp_root
    pattern = pattern.lower()
    i = 0
    while i < len(pattern):
        matched = False
        for label, child in node.children.items():
            label_lower = label.lower()
            if pattern.startswith(label_lower, i):
                i += len(label_lower)
                node = child
                matched = True
                break
            elif label_lower.startswith(pattern[i:]):
                return False
        if not matched:
            return False
    return node.eow


def print_compressed(comp_root, prefix="root"):
    """Pretty-print compressed trie edges."""
    for label, child in comp_root.children.items():
        print(f"{prefix} --[{label}]--> (eow={child.eow}, idx={child.indexes[:5]})")
        print_compressed(child, prefix + "/" + label)


# ---------------- Example usage ----------------
text = "BanAna"
uncompressed = build_suffix_trie(text)
compressed = compress(uncompressed)

print("Compressed suffix trie edges:")
print_compressed(compressed)

patterns = ["ana", "NA", "Ban", "A", "Nana", "X"]
print("\nPattern -> Starting indices (case-insensitive)")
for p in patterns:
    print(f"{p:7} -> {search_positions(compressed, p)}")

print("\nSearch results (pattern -> substring?, is_full_suffix?)")
tests = ["n", "ANA", "Nana", "BAN", "banana", "A", "NA", "AnAnA", "x"]
for t in tests:
    print(f"{t:7} -> {search_substring(compressed, t):5} , {search_is_suffix(compressed, t):5}")
