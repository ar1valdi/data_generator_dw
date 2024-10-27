from datetime import date

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

TITLES = [None, "Licencjat", "Inżynier", "Magister", "Magister Inżynier", "Doktor", "Doktor Habilitowany", "Profesor"]
TITLES_WORKER_PROB = [0, 1, 5, 1, 15, 50, 19, 9]
TITLES_STUDENT_PROB = [60, 28, 2, 2, 8, 0, 0, 0]

# STUDENTS
STUDYING_STUDENTS_PROB = [80, 20]  # true, false

DATE_OF_UNIVERSITY_START = date(1970, 1, 1)
MIN_STUDY_START_AGE = {
    "BACHELORS": 18,
    "MASTERS": 21,
    "DOCTORS": 23
}
MAX_STUDY_START_AGE = {
    "BACHELORS": 30,
    "MASTERS": 40,
    "DOCTORS": 50
}
STUDIES_STUDY_TIME = {
    "BACHELORS": 3.5,
    "MASTERS": 2,
    "DOCTORS": 4
}

# WORKERS
MIN_WORKER_AGE = 23
MAX_WORKER_AGE = 70
WORKER_STILL_WORKING_PROB = [60, 40]  # True, False
