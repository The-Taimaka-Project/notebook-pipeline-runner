import src.email as email
from src import lock
from src import pipeline
from src.colors import BOLD, END, RED
import os
import argparse
import datetime
from dotenv import load_dotenv

load_dotenv()


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
    main_path = os.path.dirname(os.path.abspath(__file__)) #path to main.py being run

    LOCK_FILE = '/tmp/pipeline.lock'
    LOG_DIRECTORY = main_path+'/logs'
    OUTPUT_DIR = main_path+'/out'
    ERROR_HOLD = main_path+'/out/error.txt'

    email.send_email('PIPELINE IS INITIATING',
                     '<strong>Pipeline began running at %s</strong>' % datetime.datetime.now())

    parser = argparse.ArgumentParser(description="Run a pipeline of notebooks.")
    parser.add_argument('--bypass-confirm', action='store_true', help='Bypass the confirmation prompt.')
    args = parser.parse_args()

    lock_success, lock_file_IO_wrapper = lock.obtain_lock(LOCK_FILE)

    if not lock_success:
        print("Another instance of the script is already running.")
        exit()

    if os.path.isfile(ERROR_HOLD):
        print(RED +
              "There was an error the last time the pipeline was run. Please make sure the error was fixed."
              + END)
        print("Once the error is fixed, delete the status file found at {0} and run the pipeline again."
              .format(ERROR_HOLD))
        exit()

    notebooks = ['/notebooks/admit_updater.ipynb',
                 '/notebooks/weekly_updater.ipynb',
                 '/notebooks/itp_arrival_updater.ipynb',
                 '/notebooks/itp_discharge_updater.ipynb',
                '/notebooks/biometrics_updater.ipynb',
                '/notebooks/mmh_updater.ipynb',
                 '/notebooks/current_crawler.ipynb',
                 '/notebooks/attachment_updater.ipynb'
                 ] #use relative paths from main.py here, with no leading .
    notebooks = [main_path + i for i in notebooks]

    if not args.bypass_confirm and not confirm_run(notebooks):
        print("Exiting...")
        exit()

    pipeline.run_pipeline(LOG_DIRECTORY, OUTPUT_DIR, ERROR_HOLD, notebooks, main_path+"/notebooks/")

    lock.release_lock(LOCK_FILE, lock_file_IO_wrapper)

    print("Pipeline finished. Check out the output directory at {0} for the results.\nLogs found at {1}"
          .format(BOLD + OUTPUT_DIR + END,
                  BOLD + LOG_DIRECTORY + END))
