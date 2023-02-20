import fcntl
import os


def obtain_lock(lock_file) -> bool:
    lock_file = open(lock_file, 'w')

    try:
        fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        print("Another instance of the script is already running.")
        return False

    print("Lock acquired by pid: " + str(os.getpid()))


def release_lock(lock_file):
    print("Releasing lock")
    fcntl.flock(lock_file, fcntl.LOCK_UN)
    lock_file.close()
    os.remove(lock_file)

    print("Lock released by pid: " + str(os.getpid()))
