import csv
import os
import threading
from datetime import date, datetime

import models.csv_models
import models.sql_models

csv_lock = threading.Lock()
sql_lock = threading.Lock()
prev_student_lock = threading.Lock()
prev_course_lock = threading.Lock()


def write_to_csv(array, filename, prefix):
    filename = f"results/{prefix}_{filename}.csv"
    fieldnames = array[0].__dict__.keys()

    with csv_lock:
        add_headers = not os.path.isfile(filename)
        with open(filename, "a", newline='', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if add_headers:
                writer.writeheader()

            for obj in array:
                writer.writerow(obj.__dict__)


def prepare_query_line(fieldnames, obj, end):
    values = []
    for field in fieldnames:
        value = getattr(obj, field)
        if isinstance(value, date):
            value = f"'{value.strftime('%Y-%m-%d')}'"
        elif value is None:
            value = 'NULL'
        else:
            value = repr(value)
        values.append(value)

    return f"({' , '.join(values)}){end}"


def write_to_sql(array, table_name, prefix):
    filename = f"results/{prefix}_{table_name}_inserts.sql"
    query = ""
    fieldnames = array[0].__dict__.keys()

    with sql_lock:
        if not os.path.isfile(filename):
            query = f"INSERT INTO {table_name} ({','.join(fieldnames)}) VALUES\n"
        else:
            query = f",\n"

        with open(filename, "a", encoding="utf-8") as sqlfile:
            for obj in array[:-1]:
                query += prepare_query_line(fieldnames, obj, ",\n")
            query += prepare_query_line(fieldnames, array[-1], "")

            sqlfile.write(query)


def __parse_date(date_string):
    if date_string:
        try:
            return datetime.strptime(date_string, "%Y-%m-%d").date()
        except Exception:
            return None
    return None


def get_all_saved_students(filename):
    with prev_student_lock:
        students_csv = []
        with open(f"results/{filename}.csv", newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                student_csv = models.csv_models.StudentCSV(
                    id=int(row["id"]),
                    imie=row["imie"],
                    drugie_imie=row["drugie_imie"],
                    nazwisko=row["nazwisko"],
                    tytul_naukowy=row["tytul_naukowy"],
                    data_urodzenia=__parse_date(row["data_urodzenia"]),
                    data_rozpoczecia_studiow=__parse_date(row["data_rozpoczecia_studiow"]),
                    data_zakonczenia_studiow=__parse_date(row["data_zakonczenia_studiow"])
                )
                students_csv.append(student_csv)

        students_sql = []
        with open(f"results/{filename}_inserts.sql", newline='', encoding='utf-8') as sqlfile:
            reader = sqlfile.readlines()[1:]
            for row in reader:
                fields = row.split(" , ")
                id = int(fields[0][1:])
                imie = fields[1]
                imie2 = fields[2]
                nazwisko = fields[3]
                data_urodzenia = __parse_date(fields[4][1:-1])
                study_name = fields[5]
                study_year = fields[6].strip()[:-2]
                student_sql = models.sql_models.StudentSQL(id, imie, imie2, nazwisko, data_urodzenia, study_name, study_year)
                student_sql.nazwa_kierunku_studiow = study_name
                student_sql.rok_rozpoczecia_kierunku_studiow = int(study_year)
                students_sql.append(student_sql)

        return students_csv, students_sql


def get_all_saved_courses(filename):
    with prev_course_lock:
        courses = []
        with open(f"results/{filename}_inserts.sql", newline='', encoding='utf-8') as sqlfile:
            reader = sqlfile.readlines()[1:]
            for row in reader:
                fields = row[1:-2].split(" , ")
                nazwa = fields[0]
                godziny = int(fields[1])
                ects = int(fields[2])
                id = int(fields[3])
                data_utworzenia = __parse_date(fields[4][1:-1])
                id_prow = int(fields[5])
                nazwa_kier = fields[6]
                rok_kier = int(fields[7][:-2])
                course = models.sql_models.Kurs(
                    nazwa, godziny, ects, id, data_utworzenia, id_prow, nazwa_kier, rok_kier
                )
                courses.append(course)

        return courses


