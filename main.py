from src import lock
from src import pipeline
from src.colors import BOLD, END, RED


def confirm_run(notebooks):
    print("The following notebooks will be run in the following order: ")
    index = 0
    for notebook in notebooks:
        print(index, ": " + notebook.split('/')[-1])
        index += 1

    # ask user to confirm by pressing y or n to run the pipeline
    print(BOLD + RED + "Please confirm that the order of the pipeline is correct." + END)
    print("Do you want to run this pipeline? (y/n)")
    while True:
        user_input = input()
        if(user_input == 'y'):
            return True
        elif(user_input == 'n'):
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")


if(__name__ == '__main__'):
    LOCK_FILE = '/tmp/pipeline.lock'
    LOG_DIRECTORY = './logs'
    OUTPUT_DIR = './out'

    lock_success, lock_file_IO_wrapper = lock.obtain_lock(LOCK_FILE)

    if not lock_success:
        print("Another instance of the script is already running.")
        exit()

    notebooks = ['./notebooks/notebook.ipynb',
                 './notebooks/notebook2.ipynb',
                 './notebooks/notebook4.ipynb',
                 './notebooks/notebookERROR.ipynb',
                 ]

    if not confirm_run(notebooks):
        print("Exiting...")
        exit()

    pipeline.run_pipeline(LOG_DIRECTORY, OUTPUT_DIR, notebooks)

    lock.release_lock(LOCK_FILE, lock_file_IO_wrapper)

    print("Pipeline finished. Check out the output directory at {0} for the results.\nLogs found at {1}"
          .format(BOLD + OUTPUT_DIR + END,
                  BOLD + LOG_DIRECTORY + END))
