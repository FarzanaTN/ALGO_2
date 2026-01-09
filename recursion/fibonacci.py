def fibonacci(n):
    """Return the nth Fibonacci number using recursion.

    The Fibonacci sequence is defined as:
    F(0) = 0
    F(1) = 1
    F(n) = F(n-1) + F(n-2) for n > 1

    Args:
        n (int): The position in the Fibonacci sequence.

    Returns:
        int: The nth Fibonacci number.
    """
    if n < 0:
        raise ValueError("Input should be a non-negative integer.")
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)

def fib_memo(n, memo={}):
    # Check if value already computed
    if n in memo:
        return memo[n]
    
    # Base cases
    if n <= 1:
        return n
    
    # Recursive computation with memoization
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]

def fib_dp(n):
    if n <= 1:
        return n
    
    # Create a DP table to store Fibonacci values
    dp = [0] * (n + 1)
    dp[0] = 0
    dp[1] = 1

    # Fill the table iteratively
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]
