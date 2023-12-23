import multiprocessing
import time
import os
from state import Controller
import subprocess

def run_hrReader():
    with open('hrReader_output.txt', 'w') as file:
        subprocess.run(['python', 'database/hrReader.py'], stdout=file, stderr=subprocess.STDOUT)

def run_backend():
    with open('backend_output.txt', 'w') as file:
        subprocess.run(['python', 'database/backend.py'], stdout=file, stderr=subprocess.STDOUT)

if __name__ == '__main__':
    hrReader_process = multiprocessing.Process(target=run_hrReader)
    backend_process = multiprocessing.Process(target=run_backend)

    hrReader_process.start()
    backend_process.start()

    controller = Controller()
    controller.loop()

    hrReader_process.join()
    backend_process.join()