import os
import threading
from data_export_import import recreate_bulk_load_file, generate_full_db_script, write_to_csv
from generator.batch_generator import generate_batch
from generator.generation_config import T1_DATES, T2_DATES, T1_THREADS, T2_THREADS
from generator.generation_methods import generate_full_date_range_for_dw


def go():
    # create results directory if it doesn't exist
    if not os.path.isdir("results"):
        os.makedirs("results")

    # clean existing files
    for filename in os.listdir("results"):
        file_path = os.path.join("results", filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    # T1 define thread num
    threads = []
    threads_num = T1_THREADS

    # T1 run generation
    for i in range(threads_num):
        thread = threading.Thread(target=generate_batch, args=(T1_DATES, "T1", None))
        threads.append(thread)
        thread.start()

    # T1 wait for all threads to finish
    for thread in threads:
        thread.join()

    # T2 define thread pool
    threads_num = T2_THREADS

    # T2 run generation
    for i in range(threads_num):
        thread = threading.Thread(target=generate_batch, args=(T2_DATES, "T2", "T1"))
        threads.append(thread)
        thread.start()

    # T2 wait for all threads to finish
    for thread in threads:
        thread.join()

    # create sql query
    recreate_bulk_load_file(2, "results/aa_bulk_inserts.sql")
    generate_full_db_script("database_scripts/drop_tables.sql",
                            "database_scripts/create_tables.sql",
                            "results/aa_bulk_inserts.sql",
                            "results/aa_full_db_recreation.sql")

    dates = generate_full_date_range_for_dw(T1_DATES["start"].year, T2_DATES["end"].year)
    write_to_csv(dates, "ab_dates")


go()
print("Complete")






