from . import lock
from . import pipeline

if(__name__ == '__main__'):
    LOCK_FILE = '/tmp/pipeline.lock'
    LOG_FILE = './log.txt'

    lock_success = lock.obtain_lock(LOCK_FILE)

    if(not lock_success):
        print("Another instance of the script is already running.")
        exit()

    notebooks = ['../notebook.ipynb']
    pipeline.run_pipeline(LOG_FILE, notebooks)

    lock.release_lock(LOCK_FILE)
