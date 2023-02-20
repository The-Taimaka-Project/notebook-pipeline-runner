from src import lock
from src import pipeline
from src.colors import color

if(__name__ == '__main__'):
    LOCK_FILE = '/tmp/pipeline.lock'
    LOG_FILE = './logs/log.txt'
    OUTPUT_DIR = './out'

    print("Running pipeline...\n")

    lock_success, lock_file_IO_wrapper = lock.obtain_lock(LOCK_FILE)

    if(not lock_success):
        print("Another instance of the script is already running.")
        exit()

    notebooks = ['./notebooks/notebook.ipynb', './notebooks/notebook2.ipynb']
    pipeline.run_pipeline(LOG_FILE, OUTPUT_DIR, notebooks)

    lock.release_lock(LOCK_FILE, lock_file_IO_wrapper)

    print("Pipeline finished. Check out the output directory at {0} for the results. \n Logs found at {1}"
          .format(color.BOLD + OUTPUT_DIR + color.END,
                  color.BOLD + LOG_FILE + color.END))
