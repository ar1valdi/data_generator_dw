import csv


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
            values = [repr(getattr(obj, field)) for field in fieldnames]  # Use repr to handle string quoting
            query = f"({', '.join(values)})"
            if obj != last_element:
                query += ",\n"
            else:
                query += ";"

            sqlfile.write(query)

