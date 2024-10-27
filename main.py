import os
import threading
from generator.batch_generator import generate_batch


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
threads_num = 5

# run generation
for i in range(threads_num):
    thread = threading.Thread(target=generate_batch)
    threads.append(thread)
    thread.start()

# wait for all threads to finish
for thread in threads:
    thread.join()

print("Complete")






