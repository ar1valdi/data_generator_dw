import os
import threading
from generator.batch_generator import generate_batch
from generator.generation_config import T1_DATES, T2_DATES, T1_THREADS, T2_THREADS


def go():
    # create results directory if it doesn't exist
    if not os.path.isdir("results"):
        os.makedirs("results")

    # clean existing files
    for filename in os.listdir("results"):
        file_path = os.path.join("results", filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    # define thread num
    threads = []
    threads_num = T1_THREADS

    # run generation
    for i in range(threads_num):
        thread = threading.Thread(target=generate_batch, args=(T1_DATES, "T1", None))
        threads.append(thread)
        thread.start()

    # wait for all threads to finish
    for thread in threads:
        thread.join()

    threads_num = T2_THREADS

    # run generation
    for i in range(threads_num):
        thread = threading.Thread(target=generate_batch, args=(T2_DATES, "T2", "T1"))
        threads.append(thread)
        thread.start()

    # wait for all threads to finish
    for thread in threads:
        thread.join()


go()
print("Complete")






