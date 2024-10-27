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
studies = []
courses = []
faculties = []
c1 = CourseLexicon()
s1 = StudyLexicon()

for i in range(10):
    try:
        students.append(generate_student())
        workers.append(generate_worker())
        faculties.append(generate_faculty(c1))
        studies.append(generate_study(s1, 1990, 2000))
        courses.append(generate_course(c1, date(1990, 1, 1), date(2000,1,1)))
    except Exception as e:
        print("something went wrong, skipping one generation", e)


write_to_csv(students)
write_to_csv(workers)
write_to_csv(faculties)
write_to_csv(courses)
write_to_csv(studies)

