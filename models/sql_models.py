class Katedra:
    def __init__(self, nazwa):
        self.nazwa = nazwa


class PracownikSQL:
    def __init__(self, imie, drugie_imie, nazwisko, tytul_naukowy, id, nazwa_katedry):
        self.imie = imie
        self.drugie_imie = drugie_imie
        self.nazwisko = nazwisko
        self.tytul_naukowy = tytul_naukowy
        self.id = id
        self.nazwa_katedry = nazwa_katedry

    @staticmethod
    def from_PracownikCSV(p):
        return PracownikSQL(p.imie, p.drugie_imie, p.nazwisko, p.tytul_naukowy, p.id, None)


class Kurs:
    def __init__(self, nazwa, ilosc_godzin, ects, id, data_utworzenia, odpowiedzialny_pracownik_id, nazwa_przypisanego_kierunku, rok_rozpoczecia_kierunku):
        self.nazwa = nazwa
        self.ilosc_godzin = ilosc_godzin
        self.liczba_ects = ects
        self.id = id
        self.data_utworzenia = data_utworzenia
        self.id_prowadzacego = odpowiedzialny_pracownik_id
        self.nazwa_kierunku = nazwa_przypisanego_kierunku
        self.rok_rozpoczecia_kierunku = rok_rozpoczecia_kierunku


class Kierunek:
    def __init__(self, nazwa, rok_rozpoczecia):
        self.nazwa = nazwa
        self.rok_rozpoczecia = rok_rozpoczecia


class StudentSQL:
    def __init__(self, id, imie, drugie_imie, nazwisko, data_urodzenia, nazwa_kierunku, rok_rozpoczecia_kierunku_studiow):
        self.id = id
        self.imie = imie
        self.drugie_imie = drugie_imie
        self.nazwisko = nazwisko
        self.data_urodzenia = data_urodzenia
        self.nazwa_kierunku_studiow = nazwa_kierunku
        self.rok_rozpoczecia_kierunku_studiow = rok_rozpoczecia_kierunku_studiow

    @staticmethod
    def from_StudentCSV(s):
        return StudentSQL(s.id, s.imie, s.drugie_imie, s.nazwisko, s.data_urodzenia, None, None)


class UdzialyWKursach:
    def __init__(self, id_kursu, id_studenta, ocena, data_dolaczenia, data_zakonczenia):
        self.id_kursu = id_kursu
        self.id_studenta = id_studenta
        self.ocena = ocena
        self.data_dolaczenia = data_dolaczenia
        self.data_zakonczenia = data_zakonczenia

