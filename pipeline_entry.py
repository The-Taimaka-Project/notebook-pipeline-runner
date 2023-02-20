from src import lock
from src import pipeline

if(__name__ == '__main__'):
    LOCK_FILE = '/tmp/pipeline.lock'
    LOG_FILE = './logs/log.txt'

    lock_success, lock_file_IO_wrapper = lock.obtain_lock(LOCK_FILE)

    if(not lock_success):
        print("Another instance of the script is already running.")
        exit()

    notebooks = ['./notebooks/notebook.ipynb']
    pipeline.run_pipeline(LOG_FILE, notebooks)

    lock.release_lock(LOCK_FILE, lock_file_IO_wrapper)
