class Katedra:
    def __init__(self, nazwa):
        self.nazwa = nazwa


class PracownikSQL:
    def __init__(self, imie, drugie_imie, nazwisko, tytul_naukowy, id, nazwa_katedry, pesel):
        self.id = id
        self.imie = imie
        self.drugie_imie = drugie_imie
        self.nazwisko = nazwisko
        self.tytul_naukowy = tytul_naukowy
        self.nazwa_katedry = nazwa_katedry
        self.pesel = pesel

    @staticmethod
    def from_PracownikCSV(p):
        return PracownikSQL(p.imie, p.drugie_imie, p.nazwisko, p.tytul_naukowy, p.id, None, p.pesel)


class Kurs:
    def __init__(self, nazwa, ilosc_godzin, liczba_ects, id, data_utworzenia, id_prowadzacego, nazwa_przypisanego_kierunku, rok_rozpoczecia_kierunku, kod):
        self.id = id
        self.nazwa = nazwa
        self.ilosc_godzin = ilosc_godzin
        self.liczba_ects = liczba_ects
        self.data_utworzenia = data_utworzenia
        self.id_prowadzacego = id_prowadzacego
        self.nazwa_przypisanego_kierunku = nazwa_przypisanego_kierunku
        self.rok_rozpoczecia_kierunku = rok_rozpoczecia_kierunku
        self.kod = kod


class Kierunek:
    def __init__(self, nazwa, rok_rozpoczecia):
        self.nazwa = nazwa
        self.rok_rozpoczecia = rok_rozpoczecia


class StudentSQL:
    def __init__(self, id, imie, drugie_imie, nazwisko, data_urodzenia, nazwa_kierunku_studiow, rok_rozpoczecia_kierunku_studiow, pesel):
        self.id = id
        self.imie = imie
        self.drugie_imie = drugie_imie
        self.nazwisko = nazwisko
        self.data_urodzenia = data_urodzenia
        self.nazwa_kierunku_studiow = nazwa_kierunku_studiow
        self.rok_rozpoczecia_kierunku_studiow = rok_rozpoczecia_kierunku_studiow
        self.pesel = pesel

    @staticmethod
    def from_StudentCSV(s):
        return StudentSQL(s.id, s.imie, s.drugie_imie, s.nazwisko, s.data_urodzenia,
                          None, None, s.pesel)


class UdzialyWKursach:
    def __init__(self, id_kursu, id_studenta, ocena, data_dolaczenia, data_zakonczenia):
        self.id_kursu = id_kursu
        self.id_studenta = id_studenta
        self.ocena = ocena
        self.data_dolaczenia = data_dolaczenia
        self.data_zakonczenia = data_zakonczenia

