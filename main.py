import csv

from generator.generation_methods import *


def write_to_csv(array):
    filename = f"{next(name for name, value in globals().items() if value is array)}.csv"
    fieldnames = array[0].__dict__.keys()

    with open(filename, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for obj in array:
            writer.writerow(obj.__dict__)


students = []
workers = []

for i in range(10):
    try:
        students.append(generate_student())
        workers.append(generate_worker())
    except Exception:
        print("something went wrong, skipping one generation")


write_to_csv(students)
write_to_csv(workers)

