import threading, time, logging

from metamask_bf_v6 import brute_force_metamask
from threading import Thread


# write all logs to app.log
logging.basicConfig(
    filename="app.log", filemode="a", format="%(name)s - %(levelname)s - %(message)s"
)

MAX_THREADS = 4
REFRESH_TIME_MINUTES = 25

# number of threads to avoid busy waiting in main process
sema = threading.Semaphore(MAX_THREADS)

# packaging function to be executed with semaphore and logging
def func_executor(sema):
    try:
        # function returns automatically after "time_limit_seconds"
        brute_force_metamask(
            starting_unix_timestamp=int(time.time()),
            time_limit_seconds=REFRESH_TIME_MINUTES * 60,
        )
        # release semaphore so that other threads can spawn
        sema.release()
    except Exception as e:
        logging.error(e)


while True:
    # keep spawning threads if there are less than MAX_THREADS threads
    sema.acquire()
    print("Thread Released: Starting new thread")
    Thread(target=func_executor, args=[sema]).start()
