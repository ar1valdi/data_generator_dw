from enum import Enum
import random
from faker import Faker
import datetime

from models.sql_models import *

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

    def generate_double_concord(self, case):
        gender = self.pickGender()
        match gender:
            case GrammaticalGender.MASCULINE:
                return random.choice(self.masc_sing_nouns)[case] + " " + random.choice(self.masc_sing_adjectives)[case] + " i " + random.choice(self.masc_sing_adjectives)[case]
            case GrammaticalGender.FEMININE:
                return random.choice(self.fem_sing_nouns)[case] + " " + random.choice(self.fem_sing_adjectives)[case] + " i " + random.choice(self.fem_sing_adjectives)[case]
            case GrammaticalGender.NEUTER:
                return random.choice(self.neut_sing_nouns)[case] + " " + random.choice(self.neut_sing_adjectives)[case] + " i " + random.choice(self.neut_sing_adjectives)[case]
            case GrammaticalGender.MASCULINEPERSONAL:
                return random.choice(self.masc_plur_nouns)[case] + " " + random.choice(self.masc_plur_adjectives)[case] + " i " + random.choice(self.masc_plur_adjectives)[case]
            case GrammaticalGender.NONMASCULINEPERSONAL:
                return random.choice(self.nonmasc_plur_nouns)[case] + " " + random.choice(self.nonmasc_plur_adjectives)[case] + " i " + random.choice(self.nonmasc_plur_adjectives)[case]
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

    return Kurs(name, hours, ects, id, creation_date, worker, assigned_study)

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
    
    return Kierunek(name, year) 

