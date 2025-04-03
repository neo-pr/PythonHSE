from multiprocessing import Process, Queue, freeze_support
import time
import codecs


def process_a(queue_a, queue_b):
    for msg in iter(queue_a.get, "exit"):
        time.sleep(1)
        queue_b.put(msg.lower())


def process_b(queue_b, m):
    for msg in iter(queue_b.get, "exit"):
        coded_msg = codecs.encode(msg, "rot_13")
        print(f"\n{coded_msg}\n] ", end="")
        m.put(coded_msg)


def main():
    queue_a = Queue()
    queue_b = Queue()
    m = Queue()  # main queue

    # child processes
    pa = Process(target=process_a, args=(queue_a, queue_b))
    pb = Process(target=process_b, args=(queue_b, m))

    # starting child processes
    for process in [pa, pb]:
        process.start()

    # main process
    # while True:
    #     msg = input('] ')
    #     if msg == 'exit':
    #         break
    #     queue_a.put(msg)

    # main process
    while (msg := input("] ")) != "exit":
        queue_a.put(msg)

    queue_a.put(msg)
    queue_b.put(msg)

    # terminating processes
    for process in [pa, pb]:
        process.join()


if __name__ == "__main__":
    freeze_support()
    main()
