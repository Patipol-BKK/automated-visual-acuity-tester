import os
from multiprocessing import Process
import time

def transcribe_run():
    os.system('python assemblyai_transcribe.py')

def display_run():
    os.system('python display_assemblyai.py')

if __name__ == '__main__':
    p1 = Process(target=transcribe_run)
    p2 = Process(target=display_run)
    p1.start()
    time.sleep(1)
    p2.start()
