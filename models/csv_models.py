class PracownikCSV:
    def __init__(self, id, imie, drugie_imie, nazwisko, tytul_naukowy, data_urodzenia, data_zatrudnienia,
                 data_zakonczenia_pracy, numer_umowy, pesel, data_dodania_rekordu):
        self.id = id
        self.imie = imie
        self.drugie_imie = drugie_imie
        self.nazwisko = nazwisko
        self.tytul_naukowy = tytul_naukowy
        self.data_urodzenia = data_urodzenia
        self.data_zatrudnienia = data_zatrudnienia
        self.data_zakonczenia_pracy = data_zakonczenia_pracy
        self.numer_umowy = numer_umowy
        self.pesel = pesel
        self.data_dodania_rekordu = data_dodania_rekordu


class StudentCSV:
    def __init__(self, id, imie, drugie_imie, nazwisko, tytul_naukowy, data_urodzenia, data_rozpoczecia_studiow,
                 data_zakonczenia_studiow, stopien_studiow, pesel, data_dodania_rekordu):
        self.id = id
        self.imie = imie
        self.drugie_imie = drugie_imie
        self.nazwisko = nazwisko
        self.tytul_naukowy = tytul_naukowy
        self.data_urodzenia = data_urodzenia
        self.data_rozpoczecia_studiow = data_rozpoczecia_studiow
        self.data_zakonczenia_studiow = data_zakonczenia_studiow
        self.stopien_studiow = stopien_studiow
        self.pesel = pesel
        self.data_dodania_rekordu = data_dodania_rekordu


class Data:
    def __init__(self, id, dzien, miesiac, numer_miesiaca, rok):
        self.id = id
        self.dzien = dzien
        self.miesiac = miesiac
        self.numer_miesiaca = numer_miesiaca
        self.rok = rok

