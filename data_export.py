import csv
import os
import threading
from datetime import date

csv_lock = threading.Lock()
sql_lock = threading.Lock()


def write_to_csv(array, filename):
    filename = f"results/{filename}.csv"
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
            value = value.strftime('%Y-%m-%d')
        elif value is None:
            value = 'NULL'
        else:
            value = repr(value)
        values.append(value)

    return f"({', '.join(values)}){end}"


def write_to_sql(array, table_name):
    filename = f"results/{table_name}_inserts.sql"
    query = ""
    fieldnames = array[0].__dict__.keys()

    with sql_lock:
        if not os.path.isfile(filename):
            query = f"INSERT INTO {table_name} ({', '.join(fieldnames)}) VALUES\n"

        with open(filename, "a", encoding="utf-8") as sqlfile:
            for obj in array[:-1]:
                query += prepare_query_line(fieldnames, obj, ",\n")
            query += prepare_query_line(fieldnames, array[-1], ";\n")

            sqlfile.write(query)

