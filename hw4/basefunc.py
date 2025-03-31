def fib(n):
    # Simple function that returns n-th element in Fibonacci sequence

    assert n > 0, "It stars with one..."
    n_prev, n_cur = 0, 1
    for _ in range(n - 1):
        n_cur, n_prev = n_cur + n_prev, n_cur

    return n_cur
