from generator.generation_methods import *
from data_export import *


students = []
students_sql = []
workers = []
workers_sql = []
studies = []
courses = []
faculties = []
c1 = CourseLexicon()
s1 = StudyLexicon()

for i in range(10):
    try:
        s = generate_student()
        students.append(s)
        students_sql.append(sql_models.StudentSQL.from_StudentCSV(s))
        w = generate_worker()
        workers.append(w)
        workers_sql.append(sql_models.PracownikSQL.from_PracownikCSV(w))
        faculties.append(generate_faculty(c1))
        studies.append(generate_study(s1, 1990, 2000))
        courses.append(generate_course(c1, date(1990, 1, 1), date(2000,1,1)))
    except Exception as e:
        print("something went wrong, skipping one generation: ", e)


write_to_csv(students, globals())
write_to_csv(workers, globals())
write_to_sql(faculties, "Katedry")
write_to_sql(courses, "Kursy")
write_to_sql(studies, "Kierunki")
write_to_sql(workers_sql, "Pracownicy")
write_to_sql(students_sql, "Studenci")



