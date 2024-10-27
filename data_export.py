import csv
from datetime import date


def write_to_csv(array, globals):
    filename = f"{next(name for name, value in globals.items() if value is array)}.csv"
    fieldnames = array[0].__dict__.keys()

    with open(filename, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for obj in array:
            writer.writerow(obj.__dict__)


def write_to_sql(array, table_name):
    filename = f"{table_name}_inserts.sql"

    with open(filename, "w", encoding="utf-8") as sqlfile:
        fieldnames = array[0].__dict__.keys()
        query = f"INSERT INTO {table_name} ({', '.join(fieldnames)}) VALUES\n"
        sqlfile.write(query)
        last_element = array[-1]

        for obj in array:
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

            query = f"({', '.join(values)})"
            if obj != last_element:
                query += ",\n"
            else:
                query += ";"

        sqlfile.write(query)

