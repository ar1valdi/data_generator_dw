import csv
import os
import threading
from datetime import date, datetime

import models.csv_models
import models.sql_models

csv_lock = threading.Lock()
sql_lock = threading.Lock()
prev_student_lock = threading.Lock()


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


def get_active_student(filename):
    with prev_student_lock:
        student_csv = None
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
                if student_csv.data_zakonczenia_studiow is None:
                    break

        if student_csv is None:
            return None

        student_sql = None

        with open(f"results/{filename}_inserts.sql", newline='', encoding='utf-8') as sqlfile:
            reader = sqlfile.readlines()
            for row in reader:
                if row.startswith(f"({student_csv.id}"):
                    fields = row.split(" , ")
                    study_name = fields[5]
                    study_year = fields[6].strip()[:-2]
                    student_sql = models.sql_models.StudentSQL.from_StudentCSV(student_csv)
                    student_sql.nazwa_kierunku_studiow = study_name
                    student_sql.rok_rozpoczecia_kierunku_studiow = int(study_year)
                    break

        return student_csv, student_sql
