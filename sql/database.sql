-- DATABASE: SISTEMA SPESE PERSONALI
PRAGMA foreign_keys = ON;

-- Tabella delle categorie
CREATE TABLE IF NOT EXISTS categorie (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE
);

-- Tabella delle spese
CREATE TABLE IF NOT EXISTS spese (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    importo REAL NOT NULL CHECK (importo > 0),
    categoria_id INTEGER NOT NULL,
    descrizione TEXT,
    FOREIGN KEY (categoria_id)
        REFERENCES categorie(id)
);

-- Tabella dei budget mensili
CREATE TABLE IF NOT EXISTS budget (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mese TEXT NOT NULL,
    categoria_id INTEGER NOT NULL,
    importo REAL NOT NULL CHECK (importo > 0),
    FOREIGN KEY (categoria_id)
        REFERENCES categorie(id),
    UNIQUE (mese, categoria_id)
);

-- DATI DI ESEMPIO

INSERT OR IGNORE INTO categorie (nome)
VALUES ('Alimentari');

INSERT OR IGNORE INTO categorie (nome)
VALUES ('Trasporti');

INSERT OR IGNORE INTO categorie (nome)
VALUES ('Tempo libero');

INSERT INTO spese
(data, importo, categoria_id, descrizione)
VALUES ('2026-11-15', 25.00, 1, 'Pranzo');

INSERT INTO spese
(data, importo, categoria_id, descrizione)
VALUES ('2026-11-16', 15.00, 2, 'Biglietto autobus');

INSERT INTO spese
(data, importo, categoria_id, descrizione)
VALUES ('2026-11-17', 40.00, 3, 'Cinema');

INSERT INTO budget
(mese, categoria_id, importo)
VALUES ('2026-11', 1, 300.00);

INSERT INTO budget
(mese, categoria_id, importo)
VALUES ('2026-11', 2, 100.00);

INSERT INTO budget
(mese, categoria_id, importo)
VALUES ('2026-11', 3, 150.00);