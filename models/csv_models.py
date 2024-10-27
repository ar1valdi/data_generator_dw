class PracownikCSV:
    def __init__(self, imie, drugie_imie, nazwisko, tytul_naukowy, data_urodzenia, data_zatrudnienia, numer_umowy, data_zakonczenia_pracy):
        self.imie = imie
        self.drugie_imie = drugie_imie
        self.nazwisko = nazwisko
        self.tytul_naukowy = tytul_naukowy
        self.data_urodzenia = data_urodzenia
        self.data_zatrudnienia = data_zatrudnienia
        self.numer_umowy = numer_umowy
        self.data_zakonczenia_pracy = data_zakonczenia_pracy


class StudentCSV:
    def __init__(self, imie, drugie_imie, nazwisko, tytul_naukowy, data_urodzenia, data_rozpoczecia_studiow, data_zakonczenia_studiow):
        self.imie = imie
        self.drugie_imie = drugie_imie
        self.nazwisko = nazwisko
        self.tytul_naukowy = tytul_naukowy
        self.data_urodzenia = data_urodzenia
        self.data_rozpoczecia_studiow = data_rozpoczecia_studiow
        self.data_zakonczenia_studiow = data_zakonczenia_studiow
