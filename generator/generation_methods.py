import string
from copy import deepcopy
from enum import Enum
import random
from faker import Faker
from datetime import timedelta

from data_reader import get_active_student
from generator.thread_safe_generated_values import get_course_id, is_faculty_name_unique, is_contract_number_unique, \
    get_student_id, drop_out_used
from models import csv_models, sql_models
from generator.generation_config import *

class Lexicon:
    def __init__(self, filepaths):
        with (open(filepaths[0], 'r', encoding='utf-8') as masc_sing_nouns_file,
              open(filepaths[1], 'r', encoding='utf-8') as fem_sing_nouns_file,
              open(filepaths[2], 'r', encoding='utf-8') as neut_sing_nouns_file,
              open(filepaths[3], 'r', encoding='utf-8') as masc_plur_nouns_file,
              open(filepaths[4], 'r', encoding='utf-8') as nonmasc_plur_nouns_file,
              open(filepaths[5], 'r', encoding='utf-8') as masc_sing_adjectives_file,
              open(filepaths[6], 'r', encoding='utf-8') as fem_sing_adjectives_file,
              open(filepaths[7], 'r', encoding='utf-8') as neut_sing_adjectives_file,
              open(filepaths[8], 'r', encoding='utf-8') as masc_plur_adjectives_file,
              open(filepaths[9], 'r', encoding='utf-8') as nonmasc_plur_adjectives_file):
            masc_sing_nouns = masc_sing_nouns_file.readlines()
            fem_sing_nouns = fem_sing_nouns_file.readlines()
            neut_sing_nouns = neut_sing_nouns_file.readlines()
            masc_plur_nouns = masc_plur_nouns_file.readlines()
            nonmasc_plur_nouns = nonmasc_plur_nouns_file.readlines()

            masc_sing_adjectives = masc_sing_adjectives_file.readlines()
            fem_sing_adjectives = fem_sing_adjectives_file.readlines()
            neut_sing_adjectives = neut_sing_adjectives_file.readlines()
            masc_plur_adjectives = masc_plur_adjectives_file.readlines()
            nonmasc_plur_adjectives = nonmasc_plur_adjectives_file.readlines()

            self.noun_gender_weights = [len(nouns) for nouns in
                                        [masc_sing_nouns, fem_sing_nouns, neut_sing_nouns, masc_plur_nouns,
                                         nonmasc_plur_nouns]]

            self.masc_sing_nouns = [line.strip().split(" ") for line in masc_sing_nouns]
            self.fem_sing_nouns = [line.strip().split(" ") for line in fem_sing_nouns]
            self.neut_sing_nouns = [line.strip().split(" ") for line in neut_sing_nouns]
            self.masc_plur_nouns = [line.strip().split(" ") for line in masc_plur_nouns]
            self.nonmasc_plur_nouns = [line.strip().split(" ") for line in nonmasc_plur_nouns]

            self.masc_sing_adjectives = [line.strip().split(" ") for line in masc_sing_adjectives]
            self.fem_sing_adjectives = [line.strip().split(" ") for line in fem_sing_adjectives]
            self.neut_sing_adjectives = [line.strip().split(" ") for line in neut_sing_adjectives]
            self.masc_plur_adjectives = [line.strip().split(" ") for line in masc_plur_adjectives]
            self.nonmasc_plur_adjectives = [line.strip().split(" ") for line in nonmasc_plur_adjectives]

    def pick_gender(self):
        return random.choices([g for g in GrammaticalGender], weights=self.noun_gender_weights)[0]

    # concord = noun + adjective
    # reverse concord = adjective + noun
    # double concord = noun + adjective + 'i' + adjective

    def generate_noun(self, case):
        gender = self.pick_gender()
        match gender:
            case GrammaticalGender.MASCULINE:
                return random.choice(self.masc_sing_nouns)[case]
            case GrammaticalGender.FEMININE:
                return random.choice(self.fem_sing_nouns)[case]
            case GrammaticalGender.NEUTER:
                return random.choice(self.neut_sing_nouns)[case]
            case GrammaticalGender.MASCULINEPERSONAL:
                return random.choice(self.masc_plur_nouns)[case]
            case GrammaticalGender.NONMASCULINEPERSONAL:
                return random.choice(self.nonmasc_plur_nouns)[case]
            case _:
                return "_"

    def generate_concord(self, case):
        gender = self.pick_gender()
        match gender:
            case GrammaticalGender.MASCULINE:
                return random.choice(self.masc_sing_nouns)[case] + " " + random.choice(self.masc_sing_adjectives)[case]
            case GrammaticalGender.FEMININE:
                return random.choice(self.fem_sing_nouns)[case] + " " + random.choice(self.fem_sing_adjectives)[case]
            case GrammaticalGender.NEUTER:
                return random.choice(self.neut_sing_nouns)[case] + " " + random.choice(self.neut_sing_adjectives)[case]
            case GrammaticalGender.MASCULINEPERSONAL:
                return random.choice(self.masc_plur_nouns)[case] + " " + random.choice(self.masc_plur_adjectives)[case]
            case GrammaticalGender.NONMASCULINEPERSONAL:
                return random.choice(self.nonmasc_plur_nouns)[case] + " " + random.choice(self.nonmasc_plur_adjectives)[
                    case]
            case _:
                return "_"

    def generate_double_concord(self, case):
        gender = self.pick_gender()
        match gender:
            case GrammaticalGender.MASCULINE:
                return random.choice(self.masc_sing_nouns)[case] + " " + random.choice(self.masc_sing_adjectives)[
                    case] + " i " + random.choice(self.masc_sing_adjectives)[case]
            case GrammaticalGender.FEMININE:
                return random.choice(self.fem_sing_nouns)[case] + " " + random.choice(self.fem_sing_adjectives)[
                    case] + " i " + random.choice(self.fem_sing_adjectives)[case]
            case GrammaticalGender.NEUTER:
                return random.choice(self.neut_sing_nouns)[case] + " " + random.choice(self.neut_sing_adjectives)[
                    case] + " i " + random.choice(self.neut_sing_adjectives)[case]
            case GrammaticalGender.MASCULINEPERSONAL:
                return random.choice(self.masc_plur_nouns)[case] + " " + random.choice(self.masc_plur_adjectives)[
                    case] + " i " + random.choice(self.masc_plur_adjectives)[case]
            case GrammaticalGender.NONMASCULINEPERSONAL:
                return random.choice(self.nonmasc_plur_nouns)[case] + " " + random.choice(self.nonmasc_plur_adjectives)[
                    case] + " i " + random.choice(self.nonmasc_plur_adjectives)[case]
            case _:
                return "_"

    def generate_reverse_concord(self, case):
        words = self.generate_concord(case).split(" ")
        words.reverse()
        return ' '.join(words)

    def generate_noun_nom(self):
        return self.generate_noun(0)

    def generate_noun_gen(self):
        return self.generate_noun(1)

    def generate_noun_loc(self):
        return self.generate_noun(2)

    def generate_concord_nom(self):
        return self.generate_concord(0)

    def generate_concord_gen(self):
        return self.generate_concord(1)

    def generate_concord_loc(self):
        return self.generate_concord(2)

    def generate_reverse_concord_nom(self):
        return self.generate_reverse_concord(0)

    def generate_reverse_concord_gen(self):
        return self.generate_reverse_concord(1)

    def generate_reverse_concord_loc(self):
        return self.generate_reverse_concord(2)

    def generate_double_concord_nom(self):
        return self.generate_reverse_concord(0)

    def generate_double_concord_gen(self):
        return self.generate_reverse_concord(1)

    def generate_double_concord_loc(self):
        return self.generate_reverse_concord(2)


class CourseLexicon(Lexicon):
    def __init__(self):
        super().__init__([COURSE_MASC_SING_NOUNS_FILEPATH,
                          COURSE_FEM_SING_NOUNS_FILEPATH,
                          COURSE_NEUT_SING_NOUNS_FILEPATH,
                          COURSE_MASC_PLUR_NOUNS_FILEPATH,
                          COURSE_NONMASC_PLUR_NOUNS_FILEPATH,
                          COURSE_MASC_SING_ADJECTIVES_FILEPATH,
                          COURSE_FEM_SING_ADJECTIVES_FILEPATH,
                          COURSE_NEUT_SING_ADJECTIVES_FILEPATH,
                          COURSE_MASC_PLUR_ADJECTIVES_FILEPATH,
                          COURSE_NONMASC_PLUR_ADJECTIVES_FILEPATH])


class StudyLexicon(Lexicon):
    def __init__(self):
        super().__init__([STUDY_MASC_SING_NOUNS_FILEPATH,
                          STUDY_FEM_SING_NOUNS_FILEPATH,
                          STUDY_NEUT_SING_NOUNS_FILEPATH,
                          STUDY_MASC_PLUR_NOUNS_FILEPATH,
                          STUDY_NONMASC_PLUR_NOUNS_FILEPATH,
                          STUDY_MASC_SING_ADJECTIVES_FILEPATH,
                          STUDY_FEM_SING_ADJECTIVES_FILEPATH,
                          STUDY_NEUT_SING_ADJECTIVES_FILEPATH,
                          STUDY_MASC_PLUR_ADJECTIVES_FILEPATH,
                          STUDY_NONMASC_PLUR_ADJECTIVES_FILEPATH])


class GrammaticalGender(Enum):
    MASCULINE = 1
    FEMININE = 2
    NEUTER = 3
    MASCULINEPERSONAL = 4
    NONMASCULINEPERSONAL = 5


class Sex(Enum):
    MALE = 1
    FEMALE = 2


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


def generate_min_max_birth_date_student(title: str, date_bounds):
    studies_key = get_studies_key(title)
    min_study_start_age = MIN_STUDY_START_AGE[studies_key]
    min_date = date_bounds["start"] - timedelta(days=min_study_start_age * 365)
    max_date = date_bounds["end"] - timedelta(days=min_study_start_age * 365)
    return min_date, max_date


# generates study start and end dates based on age and studies type
def generate_study_start_end_dates(title: str, birthdate: date, date_bounds):
    fake = Faker("pl_PL")

    studies_title_key = get_studies_key(title)
    min_study_start_age = MIN_STUDY_START_AGE[studies_title_key]
    max_study_start_age = MAX_STUDY_START_AGE[studies_title_key]
    max_start_date = min(
        date_bounds["end"],
        birthdate + timedelta(days=max_study_start_age * 365)
    )
    start_date = fake.date_between(
        start_date=birthdate + timedelta(days=min_study_start_age * 365),
        end_date=max_start_date
    )

    if start_date < date_bounds["end"] - timedelta(days=int(10 * 365)):
        is_studying = False
    else:
        is_studying = random.choices([True, False], weights=STUDYING_STUDENTS_PROB, k=1)[0]

    if is_studying:
        return start_date, None

    max_end_date = min(
        date_bounds["end"] - timedelta(days=int(2 * 31)),
        start_date + timedelta(days=int(STUDIES_STUDY_TIME[studies_title_key] * 365))
    )

    if max_end_date < start_date:
        end_date = None
    else:
        end_date = fake.date_between(start_date=start_date, end_date=max_end_date)
    return start_date, end_date


def generate_student(date_range):
    fake = Faker("pl_PL")

    name1, name2, surname = generate_names_and_surname(random.choice([True, False]))
    title = generate_scientific_title(for_student=True)
    min_birth, max_birth = generate_min_max_birth_date_student(title, date_range)
    birth = fake.date_between(start_date=min_birth, end_date=max_birth)
    study_start, study_end = generate_study_start_end_dates(title, birth, date_range)
    return csv_models.StudentCSV(None, name1, name2, surname, title, birth, study_start, study_end)


def generate_employment_start_end_dates(birthdate, date_bounds):
    fake = Faker("pl_PL")

    still_working = random.choices([True, False], weights=WORKER_STILL_WORKING_PROB, k=1)[0]
    current_date = date_bounds["end"]

    min_start_date = min(
        current_date - timedelta(days=31),
        birthdate + timedelta(days=MIN_WORKER_AGE * 365)
    )
    max_start_date = current_date - timedelta(days=31)
    start_date = fake.date_between(start_date=min_start_date, end_date=max_start_date)

    if still_working:
        return start_date, None

    min_end_date = start_date + timedelta(days=1)
    max_end_date = current_date
    end_date = fake.date_between(start_date=min_end_date, end_date=max_end_date)

    return start_date, end_date


def generate_contract_number():
    tries = 0
    while True:
        letters = ''.join(random.choices(string.ascii_uppercase, k=3))
        digits = ''.join(random.choices(string.digits, k=10))
        number = f"{letters}_{digits}"
        if is_contract_number_unique(number):
            return number
        tries += 1
        if tries > 100:
            raise Exception("Couldn't create unique contract number 100 times")


def generate_worker(dates_range):
    fake = Faker("pl_PL")

    name1, name2, surname = generate_names_and_surname(random.choice([True, False]))
    title = generate_scientific_title(for_student=False)
    birth = fake.date_of_birth(minimum_age=MIN_WORKER_AGE, maximum_age=MAX_WORKER_AGE)
    empl_start, empl_end = generate_employment_start_end_dates(birth, dates_range)
    contract_number = generate_contract_number()
    return csv_models.PracownikCSV(None, name1, name2, surname, title, birth, empl_start, empl_end, contract_number)


def generate_course_name(lexicon):
    course_name_recipes = [
        lambda lex: lex.generate_concord_nom() + " w " + lex.generate_noun_loc(),
        lambda lex: lex.generate_concord_nom(),
        lambda lex: lex.generate_double_concord_nom(),
        lambda lex: lex.generate_noun_nom() + " " + lex.generate_concord_gen(),
        lambda lex: lex.generate_noun_nom() + " " + lex.generate_double_concord_gen(),
        lambda lex: lex.generate_noun_nom() + " " + lex.generate_noun_gen() + " " + lex.generate_noun_gen(),
        lambda lex: lex.generate_noun_nom() + " " + lex.generate_noun_gen() + " i " + lex.generate_noun_gen(),
        lambda lex: lex.generate_noun_nom() + " " + lex.generate_noun_gen() + " w " + lex.generate_noun_loc(),
        lambda lex: lex.generate_noun_nom() + " " + lex.generate_noun_gen(),
        lambda lex: lex.generate_noun_nom() + " " + lex.generate_reverse_concord_gen(),
        lambda lex: lex.generate_noun_nom() + " i " + lex.generate_noun_nom(),
        lambda lex: lex.generate_noun_nom() + " w " + lex.generate_concord_loc(),
        lambda lex: lex.generate_noun_nom() + " w " + lex.generate_double_concord_loc(),
        lambda lex: lex.generate_noun_nom() + " w " + lex.generate_noun_loc(),
        lambda lex: lex.generate_noun_nom() + " w " + lex.generate_reverse_concord_loc(),
        lambda lex: lex.generate_reverse_concord_nom() + " " + lex.generate_concord_gen(),
        lambda lex: lex.generate_reverse_concord_nom() + " " + lex.generate_noun_gen()
    ]
    recipe = random.choice(course_name_recipes)

    return recipe(lexicon)


def generate_study_name(lexicon):
    study_name_recipes = [
        lambda lex: lex.generate_concord_nom(),
        lambda lex: lex.generate_double_concord_nom(),
        lambda lex: lex.generate_noun_nom() + " " + lex.generate_noun_gen(),
        lambda lex: lex.generate_noun_nom() + " i " + lex.generate_concord_nom(),
        lambda lex: lex.generate_noun_nom() + " i " + lex.generate_noun_nom() + " " + lex.generate_noun_gen() + " " + lex.generate_noun_gen(),
        lambda lex: lex.generate_noun_nom() + " i " + lex.generate_noun_nom() + " " + lex.generate_noun_gen(),
        lambda lex: lex.generate_noun_nom() + " i " + lex.generate_noun_nom(),
        lambda lex: lex.generate_noun_nom() + ", " + lex.generate_noun_nom() + " i " + lex.generate_noun_nom() + " " + lex.generate_noun_gen(),
        lambda lex: lex.generate_noun_nom() + ", " + lex.generate_noun_nom() + " i " + lex.generate_noun_nom(),
        lambda lex: lex.generate_noun_nom(),
        lambda lex: lex.generate_reverse_concord_nom()
    ]
    recipe = random.choice(study_name_recipes)

    return recipe(lexicon)


def generate_faculty_name(lexicon):
    faculty_name_recipes = [
        lambda lex: lex.generate_concord_gen() + " w " + lex.generate_concord_loc(),
        lambda lex: lex.generate_concord_gen() + " w " + lex.generate_noun_loc(),
        lambda lex: lex.generate_concord_gen(),
        lambda lex: lex.generate_double_concord_gen(),
        lambda lex: lex.generate_noun_gen() + " " + lex.generate_noun_gen() + " " + lex.generate_noun_gen(),
        lambda lex: lex.generate_noun_gen() + " " + lex.generate_noun_gen(),
        lambda lex: lex.generate_noun_gen() + " i " + lex.generate_concord_gen(),
        lambda lex: lex.generate_noun_gen() + " i " + lex.generate_noun_gen(),
        lambda lex: lex.generate_noun_gen() + " w " + lex.generate_concord_loc(),
        lambda lex: lex.generate_noun_gen() + " w " + lex.generate_noun_loc(),
        lambda lex: lex.generate_noun_gen() + ", " + lex.generate_noun_gen() + " i " + lex.generate_noun_gen(),
        lambda lex: lex.generate_noun_gen()
    ]
    recipe = random.choice(faculty_name_recipes)

    return "Katedra " + recipe(lexicon)


def generate_course_base(num, workers):
    course_base = []
    course_name_set = generate_name_set(CourseLexicon(), num)
    for course_name in course_name_set:
        hours = random.randrange(10, 121, 5)
        ects = random.randint(1, 8)
        worker = random.choice(workers).id
        course_base.append(sql_models.Kurs(
            course_name,
            hours,
            ects,
            None,
            None,
            worker,
            None,
            None
        ))
    return course_base


def generate_all_studies_with_courses(lexicon, num, year_from, year_to, workers, date_bounds):
    study_name_set = generate_name_set(lexicon, num)
    studies = []
    courses = []

    for study_name in study_name_set:
        course_base = generate_course_base(COURSES_PER_STUDY, workers)

        for study_start_year in range(year_from, year_to):
            study = sql_models.Kierunek(study_name, study_start_year)
            studies.append(study)

            for c in course_base:
                course = deepcopy(c)
                course.id = get_course_id()
                delta_rok_utworzenia = random.choice([2, 1, 0])
                validated_end_date = date_bounds["end"].year - 1 if date_bounds["end"].month < 10 else date_bounds["end"].year
                rok_utworzenia = min(validated_end_date, study.rok_rozpoczecia + delta_rok_utworzenia)
                course.data_utworzenia = date(
                    rok_utworzenia,
                    random.choice([2, 10]),
                    1
                )
                course.nazwa_kierunku = study.nazwa
                course.rok_rozpoczecia_kierunku = study.rok_rozpoczecia
                courses.append(course)

    return studies, courses


def generate_name_set(lexicon, num, must_be_unique=False):
    name_set = set()
    while len(name_set) < num:

        tries = 0
        if must_be_unique:
            while True:
                gen_name = generate_faculty_name(lexicon)
                tries += 1
                if is_faculty_name_unique(gen_name):
                    break
                if tries > 100:
                    raise Exception("Couldn't create unique name 100 times")
        else:
            gen_name = generate_faculty_name(lexicon)

        name_set.add(gen_name)

    return name_set


def generate_faculty(lexicon):
    tries = 0
    while True:
        name = generate_faculty_name(lexicon)
        tries += 1
        if is_faculty_name_unique(name):
            break
        if tries > 100:
            raise Exception("Couldn't create unique faculty name 100 times")

    return sql_models.Katedra(name)


def generate_dropout(last_students_csv, date_bounds):
    if drop_out_used():
        return
    s_csv, s_sql = get_active_student(last_students_csv)
    if s_csv is None:
        return None
    s_csv.data_zakonczenia_studiow = date_bounds["end"] - timedelta(days=31)
    s_csv.id = get_student_id()
    return s_csv
