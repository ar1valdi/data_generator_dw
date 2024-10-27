from enum import Enum
import random
from faker import Faker
from datetime import datetime, timedelta, date
from models import csv_models, sql_models

MALE_NAMES_FILEPATH = 'names_surnames_data/men_names.txt'
MALE_SURNAMES_FILEPATH = 'names_surnames_data/men_surnames.txt'
FEMALE_NAMES_FILEPATH = 'names_surnames_data/women_names.txt'
FEMALE_SURNAMES_FILEPATH = 'names_surnames_data/women_surnames.txt'


class Sex(Enum):
    MALE = 1
    FEMALE = 2


TITLES = [None, "Licencjat", "Inżynier", "Magister", "Magister Inżynier", "Doktor", "Doktor Habilitowany", "Profesor"]
TITLES_WORKER_PROB = [0, 1, 5, 1, 15, 50, 19, 9]
TITLES_STUDENT_PROB = [60, 28, 2, 2, 8, 0, 0, 0]

STUDYING_STUDENTS_PROB = [80, 20]  # true, false

DATE_OF_UNIVERSITY_START = date(1970, 1, 1)
STUDENT_AGE_RANGES = {
    "BACHELORS": [18, 26],
    "MASTERS": [21, 30],
    "DOCTORS": [23, 50]
}
STUDIES_STUDY_TIME = {
    "BACHELORS": 3.5,
    "MASTERS": 2,
    "DOCTORS": 4
}
fake = Faker("pl_PL")


def generate_names_and_surname(sex: Sex):
    names_path = MALE_NAMES_FILEPATH if sex is Sex.MALE else FEMALE_NAMES_FILEPATH
    surnames_path = MALE_SURNAMES_FILEPATH if sex is Sex.MALE else FEMALE_SURNAMES_FILEPATH

    with (open(names_path, 'r', encoding='utf-8') as names_file,
          open(surnames_path, 'r', encoding='utf-8') as surnames_file):
        all_names = names_file.readlines()
        all_surnames = surnames_file.readlines()

    names = random.sample(all_names, 2)
    surnames = random.choice(all_surnames)

    return names[0].strip(), names[1].strip(), surnames.strip()


def generate_scientific_title(for_student: bool):
    prob = TITLES_STUDENT_PROB if for_student else TITLES_WORKER_PROB
    return random.choices(TITLES, weights=prob, k=1)[0]


def generate_min_max_birth_date_student(title: str):
    if title is None:
        age_range = STUDENT_AGE_RANGES["BACHELORS"]
    elif title in ["Licencjat", "Inżynier"]:
        age_range = STUDENT_AGE_RANGES["MASTERS"]
    elif title in ["Magister", "Magister Inżynier"]:
        age_range = STUDENT_AGE_RANGES["DOCTORS"]
    else:
        raise Exception("Wrong title for student")

    min_date = DATE_OF_UNIVERSITY_START - timedelta(days=age_range[0] * 365)
    max_date = datetime.now().date() - timedelta(days=age_range[0] * 365)
    return min_date, max_date


def generate_study_start_end_dates(title: str, birthdate: date):
    if title is None:
        studies_title_key = "BACHELORS"
    elif title in ["Licencjat", "Inżynier"]:
        studies_title_key = "MASTERS"
    elif title in ["Magister", "Magister Inżynier"]:
        studies_title_key = "DOCTORS"
    else:
        raise Exception("Wrong title for student")

    min_age = STUDENT_AGE_RANGES[studies_title_key][0]
    start_date = fake.date_between(start_date=birthdate + timedelta(days=min_age * 365))

    if start_date < datetime.now().date() - timedelta(days=int(10 * 365)):
        is_studying = False
    else:
        is_studying = random.choices([True, False], weights=STUDYING_STUDENTS_PROB, k=1)[0]

    if is_studying:
        return start_date, None

    max_end_date = min(
        datetime.now().date(),
        start_date + timedelta(days=int(STUDIES_STUDY_TIME[studies_title_key] * 365))
    )

    end_date = fake.date_between(start_date=start_date, end_date=max_end_date)
    return start_date, end_date


def generate_student():
    name1, name2, surname = generate_names_and_surname(random.choice([True, False]))
    title = generate_scientific_title(True)
    min_birth, max_birth = generate_min_max_birth_date_student(title)
    birth = fake.date_between(start_date=min_birth, end_date=max_birth)
    study_start, study_end = generate_study_start_end_dates(title, birth)
    return csv_models.StudentCSV(name1, name2, surname, title, birth, study_start, study_end)
