import time
import multiprocessing
from basefunc import fib


def main():
    n = 10000
    start = time.time()

    # 10 processes
    processes = [
        multiprocessing.Process(target=fib, args=(n,), name=f"process_fib-{i}")
        for i in range(10)
    ]

    # running all processes at the same time
    for p in processes:
        p.start()

    # terminating the processes
    for p in processes:
        p.join()

    # displaying the time (took more time than thread)
    print("Test function: finding the 10000th element in Fibonacci sequence.")
    print("Time for 10 processes for test function: %.4f secs" % (time.time() - start))


if __name__ == "__main__":
    main()
