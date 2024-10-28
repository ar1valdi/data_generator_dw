DROP DATABASE DataWarehouse;
USE DataWarehouse;

CREATE TABLE Katedry (
    nazwa VARCHAR(100) PRIMARY KEY
);

CREATE TABLE Pracownicy (
    id BIGINT PRIMARY KEY,
    imie VARCHAR(32) NOT NULL,
    drugie_imie VARCHAR(32),
    nazwisko VARCHAR(50) NOT NULL,
    tytul_naukowy VARCHAR(50),
    nazwa_katedry VARCHAR(100) NOT NULL,
    FOREIGN KEY (nazwa_katedry) REFERENCES Katedry(nazwa)
);

CREATE TABLE Kierunki (
    nazwa VARCHAR(150),
    rok_rozpoczecia SMALLINT,
    PRIMARY KEY (nazwa, rok_rozpoczecia)
);

CREATE TABLE Kursy (
    id BIGINT PRIMARY KEY,
    nazwa VARCHAR(100) NOT NULL,
    ilosc_godzin SMALLINT NOT NULL,
    liczba_ects SMALLINT NOT NULL,
    data_utworzenia DATE NOT NULL,
    id_prowadzacego BIGINT NOT NULL,
    nazwa_kierunku VARCHAR(150) NOT NULL,
    rok_rozpoczecia_kierunku SMALLINT NOT NULL,
    FOREIGN KEY (id_prowadzacego) REFERENCES Pracownicy(id),
    FOREIGN KEY (nazwa_kierunku, rok_rozpoczecia_kierunku) REFERENCES Kierunki(nazwa, rok_rozpoczecia)
);

CREATE TABLE Studenci (
    id BIGINT PRIMARY KEY,
    imie VARCHAR(32) NOT NULL,
    drugie_imie VARCHAR(32),
    nazwisko VARCHAR(50) NOT NULL,
    data_urodzenia DATE NOT NULL,
    nazwa_kierunku_studiow VARCHAR(150) NOT NULL,
    rok_rozpoczecia_kierunku_studiow SMALLINT NOT NULL,
    FOREIGN KEY (nazwa_kierunku_studiow, rok_rozpoczecia_kierunku_studiow) REFERENCES Kierunki(nazwa, rok_rozpoczecia)
);

CREATE TABLE UdzialyWKursach (
    id_kursu BIGINT,
    id_studenta BIGINT,
    ocena DECIMAL(2, 1),
    data_dolaczenia DATE NOT NULL,
    data_zakonczenia DATE,
    PRIMARY KEY (id_kursu, id_studenta),
    FOREIGN KEY (id_kursu) REFERENCES Kursy(id),
    FOREIGN KEY (id_studenta) REFERENCES Studenci(id)
);
