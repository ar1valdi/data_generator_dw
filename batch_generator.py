from data_export import *
from generator.generation_methods import *
from generator.thread_safe_generated_values import get_worker_id, get_student_id


def generate_batch():
    students = []
    students_sql = []
    workers = []
    workers_sql = []
    faculties = []
    c1 = CourseLexicon()
    s1 = StudyLexicon()

    # FACULTIES
    for i in range(FACULTIES_NUM):
        faculties.append(generate_faculty(s1))
    write_to_sql(faculties, "Katedry")

    # WORKERS
    for i in range(WORKERS_NUM):
        w = generate_worker()
        w_sql = sql_models.PracownikSQL.from_PracownikCSV(w)
        w_sql.id = get_worker_id()
        w_sql.nazwa_katedry = random.choice(faculties).nazwa
        workers.append(w)
        workers_sql.append(w_sql)
    write_to_csv(workers, "pracownicy")
    write_to_sql(workers_sql, "Pracownicy")

    # COURSES, STUDIES
    studies, courses = generate_all_studies_with_courses(
        c1,
        STUDIES_NAMES_NUM,
        STUDIES_YEARS_RANGE[0],
        STUDIES_YEARS_RANGE[1],
        workers_sql
    )
    write_to_sql(courses, "Kursy")
    write_to_sql(studies, "Kierunki")

    # STUDENTS
    for i in range(STUDENTS_NUM):
        s = generate_student()
        s_sql = sql_models.StudentSQL.from_StudentCSV(s)
        s_sql.id = get_student_id()
        study = random.choice(studies)
        s_sql.nazwa_kierunku_studiow = study.nazwa
        s_sql.rok_rozpoczecia_kierunku_studiow = study.rok_rozpoczecia
        students.append(s)
        students_sql.append(s_sql)
    write_to_sql(students_sql, "Studenci")
    write_to_csv(students, "studenci")
