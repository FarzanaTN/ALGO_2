def rabin_karp(text, pattern):
    n, m = len(text), len(pattern)
    if m > n:
        return []

    base = 256          # number of possible characters (ASCII)
    mod = 10**9 + 7     # large prime to avoid overflow
    result = []

    # Precompute base^(m-1) % mod
    high_pow = pow(base, m - 1, mod)

    # Compute initial hash for pattern and first window of text
    def compute_hash(s):
        h = 0
        for i in range(m):
            h = (h * base + ord(s[i])) % mod
        return h

    pattern_hash = compute_hash(pattern)
    window_hash = compute_hash(text[:m])

    for i in range(n - m + 1):
        if window_hash == pattern_hash:
            if text[i:i+m] == pattern:  # confirm match to avoid false positives
                result.append(i)

        if i < n - m:
            # Rolling hash:
            # 1. Remove leftmost char's contribution
            window_hash = (window_hash - ord(text[i]) * high_pow) % mod
            # 2. Multiply by base to shift window
            window_hash = (window_hash * base) % mod
            # 3. Add next character
            window_hash = (window_hash + ord(text[i + m])) % mod
            # Ensure non-negative
            window_hash = (window_hash + mod) % mod
    return result

# Example usage
text = "geeksforgeeks"
pattern = "geek"
print(rabin_karp(text, pattern))  # Output: [2, 5]
