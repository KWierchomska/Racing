from multiprocessing import Pool
import os
import time

def run_process(process):
    os.system('python {}'.format(process))

def main():
    processes = ('client.py', 'client2.py')
    time.sleep(1)
    pool = Pool(processes=2)
    pool.map(run_process, processes)

main()