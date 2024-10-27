import string
from enum import Enum
import random
from faker import Faker
from datetime import datetime, timedelta
from models import csv_models, sql_models
from generator.generation_config import *


class Sex(Enum):
    MALE = 1
    FEMALE = 2


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


def get_studies_key(title: str):
    if title is None:
        return "BACHELORS"
    elif title in ["Licencjat", "Inżynier"]:
        return "MASTERS"
    elif title in ["Magister", "Magister Inżynier"]:
        return "DOCTORS"
    else:
        raise Exception("Wrong title for student")


def generate_min_max_birth_date_student(title: str):
    studies_key = get_studies_key(title)
    min_study_start_age = MIN_STUDY_START_AGE[studies_key]
    min_date = DATE_OF_UNIVERSITY_START - timedelta(days=min_study_start_age * 365)
    max_date = datetime.now().date() - timedelta(days=min_study_start_age * 365)
    return min_date, max_date


# generates study start and end dates based on age and studies type
def generate_study_start_end_dates(title: str, birthdate: date):
    studies_title_key = get_studies_key(title)
    min_study_start_age = MIN_STUDY_START_AGE[studies_title_key]
    max_study_start_age = MAX_STUDY_START_AGE[studies_title_key]
    start_date = fake.date_between(
        start_date=birthdate + timedelta(days=min_study_start_age * 365),
        end_date=birthdate + timedelta(days=max_study_start_age * 365)
    )

    if start_date < datetime.now().date() - timedelta(days=int(10 * 365)):
        is_studying = False
    else:
        is_studying = random.choices([True, False], weights=STUDYING_STUDENTS_PROB, k=1)[0]

    if is_studying:
        return start_date, None

    max_end_date = min(
        datetime.now().date() - timedelta(days=int(2 * 31)),
        start_date + timedelta(days=int(STUDIES_STUDY_TIME[studies_title_key] * 365))
    )

    end_date = fake.date_between(start_date=start_date, end_date=max_end_date)
    return start_date, end_date


def generate_student():
    name1, name2, surname = generate_names_and_surname(random.choice([True, False]))
    title = generate_scientific_title(for_student=True)
    min_birth, max_birth = generate_min_max_birth_date_student(title)
    birth = fake.date_between(start_date=min_birth, end_date=max_birth)
    study_start, study_end = generate_study_start_end_dates(title, birth)
    return csv_models.StudentCSV(name1, name2, surname, title, birth, study_start, study_end)

  # noun
# concord = noun + adjective
# reverse concord = adjective + noun


def generate_course_name(lexicon):
    course_name_recipes = [
        lambda lex : lex.generate_concord_nom(),
        lambda lex : lex.generate_noun_nom() + " " + lex.generate_concord_gen(),
        lambda lex : lex.generate_noun_nom() + " " + lex.generate_noun_gen() + " " + lex.generate_noun_gen(),
        lambda lex : lex.generate_noun_nom() + " " + lex.generate_noun_gen(),
        lambda lex : lex.generate_noun_nom() + " i " + lex.generate_noun_nom(),
        lambda lex : lex.generate_noun_nom() + " w " + lex.generate_noun_loc(),
        lambda lex : lex.generate_concord_nom() + " w " + lex.generate_noun_loc(),
        lambda lex : lex.generate_noun_nom() + " w " + lex.generate_concord_loc(),
        lambda lex : lex.generate_noun_nom() + " " + lex.generate_noun_gen() + " w " + lex.generate_noun_loc(),
        lambda lex : lex.generate_noun_nom() + " " + lex.generate_noun_gen() + " i " + lex.generate_noun_gen(),
        lambda lex : lex.generate_reverse_concord_nom() + " " + lex.generate_noun_gen(),
        lambda lex : lex.generate_reverse_concord_nom() + " " + lex.generate_concord_gen(),
        lambda lex : lex.generate_noun_nom() + " " + lex.generate_reverse_concord_gen(),
        lambda lex : lex.generate_noun_nom() + " w " + lex.generate_reverse_concord_loc(),
        lambda lex : lex.generate_double_concord_nom(),
        lambda lex : lex.generate_noun_nom() + " " + lex.generate_double_concord_gen(),
        lambda lex : lex.generate_noun_nom() + " w " + lex.generate_double_concord_loc()
    ]
    recipe = random.choice(course_name_recipes)

    return recipe(lexicon)


def generate_course(lexicon, date_from, date_to):
    fake = Faker()

    name = generate_course_name(lexicon)
    hours = random.randrange(10,121,5)
    ects = random.randint(1,8)
    id = None
    creation_date = fake.date_between(date_from, date_to)
    worker = None
    assigned_study = None

    return sql_models.Kurs(name, hours, ects, id, creation_date, worker, assigned_study)


def generate_study_name(lexicon):
    study_name_recipes = [
        lambda lex : lex.generate_concord_nom(),
        lambda lex : lex.generate_noun_nom(),
        lambda lex : lex.generate_noun_nom() + " i " + lex.generate_noun_nom(),
        lambda lex : lex.generate_noun_nom() + ", " + lex.generate_noun_nom() + " i " + lex.generate_noun_nom(),
        lambda lex : lex.generate_noun_nom() + " " + lex.generate_noun_gen(),
        lambda lex : lex.generate_reverse_concord_nom(),
        lambda lex : lex.generate_double_concord_nom(),
        lambda lex : lex.generate_noun_nom() + ", " + lex.generate_noun_nom() + " i " + lex.generate_noun_nom() + " " + lex.generate_noun_gen(),
        lambda lex : lex.generate_noun_nom() + " i " + lex.generate_noun_nom() + " " + lex.generate_noun_gen(),
        lambda lex : lex.generate_noun_nom() + " i " + lex.generate_concord_nom(),
        lambda lex : lex.generate_noun_nom() + " i " + lex.generate_noun_nom() + " " + lex.generate_noun_gen() + " " + lex.generate_noun_gen()
    ]
    recipe = random.choice(study_name_recipes)

    return recipe(lexicon)


def generate_study(lexicon, year_from, year_to):
    name = generate_study_name(lexicon)
    year = random.randint(year_from, year_to)

    return sql_models.Kierunek(name, year)


def generate_employment_start_end_dates(birthdate: date):
    current_date = datetime.now().date()
    still_working = random.choices([True, False], weights=WORKER_STILL_WORKING_PROB, k=1)[0]

    min_date = birthdate + timedelta(MIN_WORKER_AGE * 365)
    max_date = min(
        current_date,
        birthdate + timedelta(MAX_WORKER_AGE * 365)
    )

    start_date = fake.date_between(start_date=min_date, end_date=max_date)
    end_date = None if still_working else fake.date_between(start_date=start_date, end_date=current_date)

    return start_date, end_date


def generate_worker_contract_number():
    letters = ''.join(random.choices(string.ascii_uppercase, k=3))
    digits = ''.join(random.choices(string.digits, k=10))
    return f"{letters}_{digits}"


def generate_worker():
    name1, name2, surname = generate_names_and_surname(random.choice([True, False]))
    title = generate_scientific_title(for_student=False)
    birth = fake.date_of_birth(minimum_age=MIN_WORKER_AGE, maximum_age=MAX_WORKER_AGE)
    empl_start_date, empl_end_date = generate_employment_start_end_dates(birth)
    contract_number = generate_worker_contract_number()
    return csv_models.PracownikCSV(name1, name2, surname, title, birth, empl_start_date, empl_end_date, contract_number)
