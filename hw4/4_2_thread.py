from concurrent.futures import ThreadPoolExecutor
from integrate import integrate
import os
import math
import time


def main():
    cpu_count = os.cpu_count()  # 4
    time_execs = {}
    start = time.time()
    for n_jobs in range(1, cpu_count * 2 + 1):
        start_jobs = time.time()
        with ThreadPoolExecutor(max_workers=n_jobs) as executor:
            # submitting the jobs to the pool
            futures = []
            for job_nb in range(1, n_jobs + 1):
                futures.append(
                    executor.submit(integrate, math.cos, 0, math.pi / 2, job_nb, n_jobs)
                )
            # getting the results
            result = 0
            for future in futures:
                result += future.result()
        time_execs[n_jobs] = {
            "time": f"{time.time() - start_jobs:.3f} secs",
            "result": result,
        }

    print("-- Detailed results -- ")
    for k, i in time_execs.items():
        print(f"max workers: {k}, time: {i['time']}, result: {i['result']}")
    print(f"\nTotal time: {time.time() - start:.3f} secs")


if __name__ == "__main__":
    main()
