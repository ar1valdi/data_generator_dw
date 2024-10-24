from enum import Enum
import random


MALE_NAMES_FILEPATH = 'names_surnames_data/men_names.txt'
MALE_SURNAMES_FILEPATH = 'names_surnames_data/men_surnames.txt'
FEMALE_NAMES_FILEPATH = 'names_surnames_data/women_names.txt'
FEMALE_SURNAMES_FILEPATH = 'names_surnames_data/women_surnames.txt'


class Sex(Enum):
    MALE = 1
    FEMALE = 2


def generate_names_and_surname(sex: Sex):
    names_path = MALE_NAMES_FILEPATH if sex is sex.MALE else FEMALE_NAMES_FILEPATH
    surnames_path = MALE_SURNAMES_FILEPATH if sex is sex.MALE else FEMALE_SURNAMES_FILEPATH

    with (open(names_path, 'r', encoding='utf-8') as names_file,
          open(surnames_path, 'r', encoding='utf-8') as surnames_file):
        all_names = names_file.readlines()
        all_surnames = surnames_file.readlines()

    imiona = random.sample(all_names, 2)
    nazwisko = random.choice(all_surnames)

    return imiona[0].strip(), imiona[1].strip(), nazwisko.strip()

