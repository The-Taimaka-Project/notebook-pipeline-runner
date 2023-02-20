import fcntl
import os
from .colors import color


def obtain_lock(lock_file):
    lock_file = open(lock_file, 'w')

    try:
        fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        print("Another instance of the script is already running.")
        return False, None

    print(color.BOLD + "Lock acquired by pid: " + color.END + str(os.getpid()))
    return True, lock_file


def release_lock(lock_file_path, lock_file_IO_wrapper):
    print("Releasing lock")
    fcntl.flock(lock_file_IO_wrapper, fcntl.LOCK_UN)
    lock_file_IO_wrapper.close()
    os.remove(lock_file_path)

    print(color.BOLD + "Lock released by pid: " + color.END + str(os.getpid()))
