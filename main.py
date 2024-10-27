import csv

from generator.generation_methods import *

students = []

for i in range(10):
    students.append(generate_student())

with open("students.csv", "w", newline='') as csvfile:
    fieldnames = students[0].__dict__.keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for student in students:
        writer.writerow(student.__dict__)
