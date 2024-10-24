from enum import Enum
import random
from faker import Faker

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


def generate_names_and_surname(sex: Sex):
    names_path = MALE_NAMES_FILEPATH if sex is Sex.MALE else FEMALE_NAMES_FILEPATH
    surnames_path = MALE_SURNAMES_FILEPATH if sex is Sex.MALE else FEMALE_SURNAMES_FILEPATH

    with (open(names_path, 'r', encoding='utf-8') as names_file,
          open(surnames_path, 'r', encoding='utf-8') as surnames_file):
        all_names = names_file.readlines()
        all_surnames = surnames_file.readlines()

    imiona = random.sample(all_names, 2)
    nazwisko = random.choice(all_surnames)

    return imiona[0].strip(), imiona[1].strip(), nazwisko.strip()


def generate_scientific_title(for_student: bool):
    prob = TITLES_STUDENT_PROB if for_student else TITLES_WORKER_PROB
    return random.choices(TITLES, weights=prob, k=1)[0]


def generate_student(date_from, date_to):
    fake = Faker()
    imie1, imie2, nazwisko = generate_names_and_surname(random.choice([True, False]))
    title = generate_scientific_title(True)
    min_age, max_age = 0, 0
    data_rozpoczecia_studiow = 0

    if title is None:
        min_age, max_age = 18, 26
    elif title in ["Licencjat", "Inżynier"]:
        min_age, max_age = 21, 30
    elif title in ["Magister", "Magister Inżynier"]:
        min_age, max_age = 23, 50

    data_urodzenia = fake.date_of_birth(minimum_age=min_age, maximum_age=max_age)
