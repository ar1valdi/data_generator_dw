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
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")

            if add_headers:
                writer.writeheader()

            for obj in array:
                row = {}
                for key, value in obj.__dict__.items():
                    if isinstance(value, date):
                        row[key] = f"{value.strftime('%Y-%m-%d')}"
                    else:
                        row[key] = value
                writer.writerow(row)


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
        with open(f"results/{filename}_CSV.csv", newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            for row in reader:
                student_csv = models.csv_models.StudentCSV(
                    id=int(row["id"]),
                    imie=row["imie"],
                    drugie_imie=row["drugie_imie"],
                    nazwisko=row["nazwisko"],
                    tytul_naukowy=row["tytul_naukowy"],
                    data_urodzenia=__parse_date(row["data_urodzenia"]),
                    data_rozpoczecia_studiow=__parse_date(row["data_rozpoczecia_studiow"]),
                    data_zakonczenia_studiow=__parse_date(row["data_zakonczenia_studiow"]),
                    stopien_studiow=row["stopien_studiow"],
                    pesel=row["pesel"]
                )
                students_csv.append(student_csv)

        students_sql = []
        with open(f"results/{filename}.csv", newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            for row in reader:
                student_sql = models.sql_models.StudentSQL(
                    id=int(row["id"]),
                    imie=row["imie"],
                    drugie_imie=row["drugie_imie"],
                    nazwisko=row["nazwisko"],
                    data_urodzenia=__parse_date(row["data_urodzenia"]),
                    nazwa_kierunku_studiow=row["nazwa_kierunku_studiow"],
                    rok_rozpoczecia_kierunku_studiow=row["rok_rozpoczecia_kierunku_studiow"],
                    pesel=row["pesel"]
                )
                students_sql.append(student_sql)

        return students_csv, students_sql


def get_all_saved_courses(filename):
    with prev_course_lock:
        courses = []
        with open(f"results/{filename}.csv", newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            for row in reader:
                course = models.sql_models.Kurs(
                    nazwa=int(row["nazwa"]),
                    ilosc_godzin=int(row["ilosc_godzin"]),
                    liczba_ects=int(row["ilosc_ects"]),
                    id=int(row["id"]),
                    data_utworzenia=__parse_date(row["data_utworzenia"]),
                    id_prowadzacego=int(row["id_prowadzacego"]),
                    nazwa_przypisanego_kierunku=row["nazwa_przypisanego_kierunku"],
                    rok_rozpoczecia_kierunku=int(row["rok_przypisanego_kierunku"])
                )
                courses.append(course)

        return courses


def recreate_bulk_load_file(timestamps_num: int, result_path):
    filenames = ["Katedry", "Pracownicy", "Kierunki", "Kursy", "Studenci", "UdzialyWKursach"]
    table_names = ["Katedry", "Pracownicy", "Kierunki", "Kursy", "Studenci", "UdzialyWKursach"]
    file_extension = ".csv"

    for i in range(1, timestamps_num+1):
        prefix = f"T{i}"
        for j in range(len(filenames)):
            abs_path = os.path.abspath(f"results/{prefix}_{filenames[j]}{file_extension}")
            query = get_bulk_query(table_names[j], abs_path)

            with open(result_path, newline='', encoding='utf-8', mode='a') as file:
                file.write(query + '\n')


def get_bulk_query(table_name: str, csv_file_path: str) -> str:
    return f"BULK INSERT {table_name} \n \
             FROM '{csv_file_path}' \n \
             WITH ( \n \
                 FIELDTERMINATOR = ';', \n \
                 ROWTERMINATOR = '\\n', \n \
                 FIRSTROW = 2, \n \
                 CODEPAGE = '65001' \n \
             );"


def generate_full_db_script(drop_path, create_path, insert_path, result_path):
    with open(create_path, newline='', encoding='utf-8', mode='r') as create, \
         open(drop_path, newline='', encoding='utf-8', mode='r') as drop, \
         open(insert_path, newline='', encoding='utf-8', mode='r') as insert, \
         open(result_path, newline='', encoding='utf-8', mode='w') as result:
        create_content = create.read()
        drop_content = drop.read()
        insert_content = insert.read()
        result.write(drop_content + '\n')
        result.write(create_content + '\n')
        result.write(insert_content + '\n')
