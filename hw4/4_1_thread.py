import time
import threading
from basefunc import fib


def main():
    n = 10000
    start = time.time()

    # 10 threads
    threads = [
        threading.Thread(target=fib, args=(n,), name=f"thread_fib-{i}")
        for i in range(10)
    ]

    # running all threads at the same time
    for t in threads:
        t.start()

    # terminating the threads
    for t in threads:
        t.join()

    # displaying the time
    print("Test function: finding the 10000th element in Fibonacci sequence.")
    print("Time for 10 threads for test function: %.4f secs" % (time.time() - start))


if __name__ == "__main__":
    main()
