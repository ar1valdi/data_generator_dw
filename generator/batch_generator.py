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
    c1 = CourseLexicon()
    s1 = StudyLexicon()

    # FACULTIES
    for i in range(FACULTIES_NUM):
        faculties.append(generate_faculty(s1))
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
        c1,
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
    for course in courses:
        for student in students_sql:
            if course.nazwa_kierunku == student.nazwa_kierunku_studiow and course.rok_rozpoczecia_kierunku == student.rok_rozpoczecia_kierunku_studiow:
                participations.append(generate_participation(course, student))
                continue

            if course.rok_rozpoczecia_kierunku == student.rok_rozpoczecia_kierunku_studiow and random.random() <= VOLUNTARY_JOIN_COURSE_PROB:
                student_in_csv = [s for s in students if student.id == s.id]

                if len(student_in_csv) == 0:
                    continue

                if student_in_csv[0].data_rozpoczecia_studiow < course.data_utworzenia:
                    if student_in_csv[0].data_zakonczenia_studiow == None or student_in_csv[0].data_zakonczenia_studiow > course.data_utworzenia:
                        participations.append(generate_participation(course, student))


            
            

    # MOŻE JAKIEŚ UPDATY (np. zmiana stopnia naukowego, zmiana nazwiska (małżeństwo))

    write_to_sql(participations, "UdzialyWKursach", file_prefix)

    if prev_prefix:
        s = generate_dropout(f"{prev_prefix}_Studenci", date_range)
        if s is None:
            return
        #print(s.id)
        write_to_csv([s], "Studenci", file_prefix)

