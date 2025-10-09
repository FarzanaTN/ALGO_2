def prefix_function(pattern):
    n = len(pattern)
    pi = [0] * n
    j = 0
    for i in range(1, n):
        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        pi[i] = j
    return pi


def kmp_search(text, pattern):
    n, m = len(text), len(pattern)
    pi = prefix_function(pattern)
    result = []

    j = 0  # index for pattern
    for i in range(n):  # index for text
        while j > 0 and text[i] != pattern[j]:
            j = pi[j - 1]

        if text[i] == pattern[j]:
            j += 1

        if j == m:
            # Pattern found ending at index i → start = i - m + 1
            result.append(i - m + 1)
            j = pi[j - 1]  # continue searching for next matches

    return result


# Example usage
if __name__ == "__main__":
    text = "aabaacaadaabaaba"
    pattern = "aaba"
    matches = kmp_search(text, pattern)
    print("Pattern found at indices:", matches)
