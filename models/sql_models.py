class Katedra:
    def __init__(self, nazwa):
        self.nazwa = nazwa


class PracownikSQL:
    def __init__(self, imie, drugieImie, nazwisko, tytul_naukowy, id, nazwa_katedry):
        self.imie = imie
        self.drugieImie = drugieImie
        self.nazwisko = nazwisko
        self.tytul_naukowy = tytul_naukowy
        self.id = id
        self.nazwa_katedry = nazwa_katedry


class Kurs:
    def __init__(self, nazwa, ilosc_godzin, ects, id, data_utworzenia, odpowiedzialny_pracownik_id, nazwa_przypisanego_kierunku):
        self.nazwa = nazwa
        self.ilosc_godin = ilosc_godzin
        self.liczba_ects = ects
        self.id = id
        self.data_utworzenia = data_utworzenia
        self.odpowiedzialny_pracownik = odpowiedzialny_pracownik_id
        self.przypisany_kierunek = nazwa_przypisanego_kierunku


class Kierunek:
    def __init__(self, nazwa, rok_rozpoczecia):
        self.nazwa = nazwa
        self.rok_rozpoczecia = rok_rozpoczecia


class StudentSQL:
    def __init__(self, id, imie, drugie_imie, nazwisko, data_urodzenia, nazwa_kierunku):
        self.id = id
        self.imie = imie
        self.drugie_imie = drugie_imie
        self.nazwisko = nazwisko
        self.data_urodzenia = data_urodzenia
        self.kierunek_studiow = nazwa_kierunku


class UdzialyWKursach:
    def __init__(self, id_kursu, id_studenta, ocena, data_dolaczenia, data_zakonczenia):
        self.id_kursu = id_kursu
        self.id_studenta = id_studenta
        self.ocena = ocena
        self.data_dolaczenia = data_dolaczenia
        self.data_zakonczenia = data_zakonczenia

