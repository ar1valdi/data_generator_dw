import string
from copy import deepcopy
from enum import Enum
import random
from faker import Faker
from datetime import timedelta, datetime

import models.csv_models
from data_export_import import get_all_saved_students
from generator.thread_safe_generated_values import get_course_id, is_faculty_name_unique, is_contract_number_unique, \
    get_student_id, drop_out_used, is_pesel_unique, is_course_code_unique
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
    MALE = True
    FEMALE = False


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


def get_stopien_studiow(title) -> str:
    key = get_studies_key(title)

    if key == "BACHELORS":
        return "Pierwszy"
    elif key == "MASTERS":
        return "Drugi"
    else:
        return "Trzeci"


def generate_student(date_range):
    fake = Faker("pl_PL")

    sex = random.choice([True, False])
    name1, name2, surname = generate_names_and_surname(sex)
    title = generate_scientific_title(for_student=True)
    stopien_studiow = get_stopien_studiow(title)
    min_birth, max_birth = generate_min_max_birth_date_student(title, date_range)
    birth = fake.date_between(start_date=min_birth, end_date=max_birth)
    study_start, study_end = generate_study_start_end_dates(title, birth, date_range)
    pesel = get_unique_pesel(fake, datetime.combine(birth, datetime.min.time()), 'M' if sex else 'F')
    add_date = fake.date_between(start_date=study_start - timedelta(days=31), end_date=study_start)
    return csv_models.StudentCSV(None, name1, name2, surname, title, birth, study_start,
                                 study_end, stopien_studiow, pesel, add_date)


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

    sex = random.choice([True, False])
    name1, name2, surname = generate_names_and_surname(sex)
    title = generate_scientific_title(for_student=False)
    birth = fake.date_of_birth(minimum_age=MIN_WORKER_AGE, maximum_age=MAX_WORKER_AGE)
    empl_start, empl_end = generate_employment_start_end_dates(birth, dates_range)
    pesel = get_unique_pesel(fake, datetime.combine(birth, datetime.min.time()), 'M' if sex else 'F')
    contract_number = generate_contract_number()
    add_date = fake.date_between(start_date=empl_start - timedelta(days=7), end_date=empl_start)
    return csv_models.PracownikCSV(None, name1, name2, surname, title, birth, empl_start,
                                   empl_end, contract_number, pesel, add_date)


def get_unique_pesel(fake, birth, sex):
    for i in range(100):
        pesel = fake.pesel(birth, sex)
        if is_pesel_unique(pesel):
            return pesel

    raise Exception("Couldn't create unique contract number 100 times")


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
    course_name_set = generate_name_set(CourseLexicon(), num, generate_course_name)
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
            None,
            None
        ))
    return course_base


def generate_all_studies_with_courses(num, year_from, year_to, workers, date_bounds):
    study_name_set = generate_name_set(StudyLexicon(), num, generate_study_name)
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
                course.nazwa_przypisanego_kierunku = study.nazwa
                course.rok_rozpoczecia_kierunku = study.rok_rozpoczecia
                course.kod = generate_course_code()
                courses.append(course)

    return studies, courses


def generate_course_code():
    for i in range(100):
        code = ''.join(random.choices(string.ascii_uppercase, k=8))
        if is_course_code_unique(code):
            return code

    raise Exception("Couldn't create unique course code 100 times")


def generate_name_set(lexicon, num, generation_method, must_be_unique=True):
    name_set = set()
    while len(name_set) < num:

        tries = 0
        if must_be_unique:
            while True:
                gen_name = generation_method(lexicon)
                tries += 1
                if is_faculty_name_unique(gen_name):
                    break
                if tries > 100:
                    raise Exception("Couldn't create unique name 100 times")
        else:
            gen_name = generation_method(lexicon)

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


def get_next_stopien_studiow(stopien):
    if stopien == "Pierwszy":
        return "Drugi"
    elif stopien == "Drugi":
        return "Trzeci"
    return None


def get_next_title(title):
    if title is None:
        return "Inżynier"
    elif title == "Inżynier":
        return "Magister Inżynier"
    elif title == "Licencjat":
        return "Magister"
    elif title in ["Magister", "Magister Inżynier"]:
        return "Doktor"
    elif title == "Doktor":
        return "Doktor Habilitowany"
    else:
        return "Profesor"


def generate_dropout(last_students_csv, date_bounds):
    if drop_out_used():
        return
    s_csv, s_sql = get_all_saved_students(last_students_csv)
    active_s = None

    for s in s_csv:
        if s.data_zakonczenia_studiow is None:
            active_s = s
            break
    if active_s is None:
        return None

    active_s.data_zakonczenia_studiow = date_bounds["end"] - timedelta(days=31)
    active_s.stopien_studiow = get_next_stopien_studiow(active_s.stopien_studiow)
    active_s.tytul_naukowy = get_next_title(active_s.tytul_naukowy)
    active_s.id = get_student_id()
    print(active_s.id)
    return active_s


def generate_participation(course, student):
    fake = Faker("pl_PL")

    grade = random.choices([2,3,3.5,4,4.5,5], weights = [1,15,20,25,20,10])[0]
    start_date = fake.date_between_dates(course.data_utworzenia, course.data_utworzenia + timedelta(30))
    end_date = fake.date_between_dates(start_date + timedelta(7), start_date + timedelta(180))

    return sql_models.UdzialyWKursach(course.id, student.id, grade, start_date, end_date)


def generate_all_participations(courses, students_sql, students):
    participations = []
    for course in courses:
        for student in students_sql:
            if course.nazwa_przypisanego_kierunku == student.nazwa_kierunku_studiow and course.rok_rozpoczecia_kierunku == student.rok_rozpoczecia_kierunku_studiow:
                participations.append(generate_participation(course, student))
                continue

            if random.random() <= VOLUNTARY_JOIN_COURSE_PROB:
                student_in_csv = [s for s in students if student.id == s.id]

                if len(student_in_csv) == 0:
                    continue

                if student_in_csv[0].data_rozpoczecia_studiow < course.data_utworzenia:
                    if student_in_csv[0].data_zakonczenia_studiow is None or student_in_csv[0].data_zakonczenia_studiow > course.data_utworzenia:
                        participations.append(generate_participation(course, student))

    return participations


def generate_full_date_range_for_dw(start_year: int, end_year: int):
    month_dict = [
        ["styczeń", 31],
        ["luty", 28],
        ["marzec", 31],
        ["kwiecień", 30],
        ["maj", 31],
        ["czerwiec", 30],
        ["lipiec", 31],
        ["sierpień", 31],
        ["wrzesień", 30],
        ["październik", 31],
        ["listopad", 30],
        ["grudzień", 31],
    ]

    # insert dummy row
    id = 2
    result_dates: [models.csv_models.Data] = [
        models.csv_models.Data(1, 1, 1, 1, 1)
    ]

    for year in range(start_year, end_year):
        for month_num in range(1, 13):
            for day_num in range(1, month_dict[month_num-1][1] + 1):
                new_date = models.csv_models.Data(
                    id,
                    day_num,
                    month_dict[month_num-1][0],
                    month_num,
                    year
                )
                result_dates.append(new_date)
                id += 1

    return result_dates
