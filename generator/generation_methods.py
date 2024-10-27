from enum import Enum
import random
from faker import Faker

from datetime import datetime, timedelta, date
from models import csv_models, sql_models

MALE_NAMES_FILEPATH = 'names_surnames_data/men_names.txt'
MALE_SURNAMES_FILEPATH = 'names_surnames_data/men_surnames.txt'
FEMALE_NAMES_FILEPATH = 'names_surnames_data/women_names.txt'
FEMALE_SURNAMES_FILEPATH = 'names_surnames_data/women_surnames.txt'

COURSE_MASC_SING_NOUNS_FILEPATH = 'courses_data/nouns/masc_sing.txt'
COURSE_FEM_SING_NOUNS_FILEPATH = 'courses_data/nouns/fem_sing.txt'
COURSE_NEUT_SING_NOUNS_FILEPATH = 'courses_data/nouns/neut_sing.txt'
COURSE_MASC_PLUR_NOUNS_FILEPATH = 'courses_data/nouns/masc_plur.txt'
COURSE_NONMASC_PLUR_NOUNS_FILEPATH = 'courses_data/nouns/nonmasc_plur.txt'

COURSE_MASC_SING_ADJECTIVES_FILEPATH = 'courses_data/adjectives/masc_sing.txt'
COURSE_FEM_SING_ADJECTIVES_FILEPATH = 'courses_data/adjectives/fem_sing.txt'
COURSE_NEUT_SING_ADJECTIVES_FILEPATH = 'courses_data/adjectives/neut_sing.txt'
COURSE_MASC_PLUR_ADJECTIVES_FILEPATH = 'courses_data/adjectives/masc_plur.txt'
COURSE_NONMASC_PLUR_ADJECTIVES_FILEPATH = 'courses_data/adjectives/nonmasc_plur.txt'

STUDY_MASC_SING_NOUNS_FILEPATH = 'studies_data/nouns/masc_sing.txt'
STUDY_FEM_SING_NOUNS_FILEPATH = 'studies_data/nouns/fem_sing.txt'
STUDY_NEUT_SING_NOUNS_FILEPATH = 'studies_data/nouns/neut_sing.txt'
STUDY_MASC_PLUR_NOUNS_FILEPATH = 'studies_data/nouns/masc_plur.txt'
STUDY_NONMASC_PLUR_NOUNS_FILEPATH = 'studies_data/nouns/nonmasc_plur.txt'

STUDY_MASC_SING_ADJECTIVES_FILEPATH = 'studies_data/adjectives/masc_sing.txt'
STUDY_FEM_SING_ADJECTIVES_FILEPATH = 'studies_data/adjectives/fem_sing.txt'
STUDY_NEUT_SING_ADJECTIVES_FILEPATH = 'studies_data/adjectives/neut_sing.txt'
STUDY_MASC_PLUR_ADJECTIVES_FILEPATH = 'studies_data/adjectives/masc_plur.txt'
STUDY_NONMASC_PLUR_ADJECTIVES_FILEPATH = 'studies_data/adjectives/nonmasc_plur.txt'

class Lexicon():
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

            self.noun_gender_weights = [len(nouns) for nouns in [masc_sing_nouns, fem_sing_nouns, neut_sing_nouns, masc_plur_nouns, nonmasc_plur_nouns]]
            
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

    def pickGender(self):
        return random.choices([g for g in GrammaticalGender], weights=self.noun_gender_weights)[0]
    
    def generate_noun(self, case):
        gender = self.pickGender()
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
        gender = self.pickGender()
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
                return random.choice(self.nonmasc_plur_nouns)[case] + " " + random.choice(self.nonmasc_plur_adjectives)[case]
            case _:
                return "_"

    def generate_noun_nom(self):
        return self.generate_noun(0)
    
    def generate_concord_nom(self):
        return self.generate_concord(0)

    def generate_noun_gen(self):
        return self.generate_noun(1)

    def generate_concord_gen(self):
        return self.generate_concord(1)

    def generate_noun_loc(self):
        return self.generate_noun(2)

    def generate_concord_loc(self):
        return self.generate_concord(2)

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

  # noun
# concord = noun + adjective

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
        lambda lex : lex.generate_noun_nom() + " " + lex.generate_noun_gen() + " w " + lex.generate_noun_loc()
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

    return Kurs(name, hours, ects, id, creation_date, worker, assigned_study)

def generate_study_name(lexicon):
    study_name_recipes = [
        lambda lex : lex.generate_concord_nom(),
        lambda lex : lex.generate_noun_nom(),
        lambda lex : lex.generate_noun_nom() + " i " + lex.generate_noun_nom(),
        lambda lex : lex.generate_noun_nom() + ", " + lex.generate_noun_nom() + " i " + lex.generate_noun_nom()
    ]
    recipe = random.choice(study_name_recipes)

    return recipe(lexicon)

def generate_study(lexicon, year_from, year_to):
    name = generate_study_name(lexicon)
    year = random.randint(year_from, year_to)
    
    return Kierunek(name, year) 
