from data_reader import *
from generator.generation_methods import *
from generator.thread_safe_generated_values import get_worker_id, get_student_id


def generate_batch(date_range, file_prefix, prev_prefix):
    students = []
    students_sql = []
    workers = []
    workers_sql = []
    faculties = []
    participations = []

    # FACULTIES
    for i in range(FACULTIES_NUM):
        faculties.append(generate_faculty(StudyLexicon()))
    write_to_sql(faculties, "Katedry", file_prefix)

    # WORKERS
    for i in range(WORKERS_NUM):
        w = generate_worker(date_range)
        w.id = get_worker_id()
        w_sql = sql_models.PracownikSQL.from_PracownikCSV(w)
        w_sql.nazwa_katedry = random.choice(faculties).nazwa
        workers.append(w)
        workers_sql.append(w_sql)
    write_to_csv(workers, "Pracownicy", file_prefix)
    write_to_sql(workers_sql, "Pracownicy", file_prefix)

    # COURSES, STUDIES
    studies, courses = generate_all_studies_with_courses(
        STUDIES_NAMES_NUM,
        date_range["start"].year,
        date_range["end"].year,
        workers_sql,
        date_range
    )
    write_to_sql(courses, "Kursy", file_prefix)
    write_to_sql(studies, "Kierunki", file_prefix)

    # STUDENTS
    for i in range(STUDENTS_NUM):
        s = generate_student(date_range)
        s.id = get_student_id()
        s_sql = sql_models.StudentSQL.from_StudentCSV(s)
        study = random.choice(studies)
        s_sql.nazwa_kierunku_studiow = study.nazwa
        s_sql.rok_rozpoczecia_kierunku_studiow = study.rok_rozpoczecia
        students.append(s)
        students_sql.append(s_sql)
    write_to_sql(students_sql, "Studenci", file_prefix)
    write_to_csv(students, "Studenci", file_prefix)

    # PARTICIPATIONS IN COURSES
    if not prev_prefix:
        participations = generate_all_participations(courses, students_sql, students)
        write_to_sql(participations, "UdzialyWKursach", file_prefix)

    else:
        courses = get_all_saved_courses(f"{prev_prefix}_Kursy")
        students, students_sql = get_all_saved_students(f"{prev_prefix}_Studenci")

        participations = generate_all_participations(courses, students_sql, students)
        write_to_sql(participations, "UdzialyWKursach", file_prefix)

        # DROPOUT
        s = generate_dropout(f"{prev_prefix}_Studenci", date_range)
        if s is None:
            return
        print(s.id)
        write_to_csv([s], "Studenci", file_prefix)

