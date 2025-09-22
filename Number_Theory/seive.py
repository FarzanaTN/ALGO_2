def sieve(n):
    # Step 1: Create an array of True values
    prime = [True] * (n + 1)   # index 0..n
    prime[0] = prime[1] = False  # 0 and 1 are not primes

    # Step 2: Mark non-primes
    p = 2
    while p * p <= n:
        if prime[p]:
            # Mark multiples of p as False
            for i in range(p * p, n + 1, p):
                prime[i] = False
        p += 1

    # Step 3: Collect primes
    primes = [i for i in range(2, n + 1) if prime[i]]

    return primes


def divisor_check(n):
    divisors = set()
    d = 1
    while d * d <= n:
        if n % d == 0:
            divisors.add(d)
            divisors.add(n // d)
        d += 1
    return sorted(divisors)

def prime_divisor_check(n):
    prime_numbers = set(sieve(n))
    divisors = set()
    d = 2
    while d * d <= n:
        if n % d == 0 : 
            if d in prime_numbers:
                divisors.add(d)
            if n // d in prime_numbers:
                divisors.add(n // d)
        d += 1
    return sorted(divisors)

def optimize_prime_divisor_check(n):
    divisors = set()
    d = 2
    while d * d <= n:
        if n % d == 0:
            print(d)
            divisors.add(d)
            while n % d == 0:   # divide out all powers of d
                n //= d
        d += 1
    if n > 1:   # if n is prime after reduction
        divisors.add(n)
    return sorted(divisors)

def prime_sum(n):
    primes = sieve(n)   # list of primes up to n
    return sum(primes)


# print(prime_divisor_check(36))
# print(optimize_prime_divisor_check(36))
print(prime_sum(5))