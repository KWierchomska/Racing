import multiprocessing
from multiprocessing import Pool
import threading
import os


def init(lock):
    global starting
    starting = lock


def run_process(process):
    starting.acquire()  # no other process can get it until it is released
    threading.Timer(1, starting.release).start()  # release in one second
    os.system('python {}'.format(process))


if __name__ == "__main__":
    processes = ('server.py', 'client.py', 'client2.py')
    pool = Pool(processes=3,
                initializer=init, initargs=[multiprocessing.Lock()])
    for _ in pool.imap_unordered(run_process, processes):
        pass
