
import sqlite3
from datetime import datetime

# Connessione al database
conn = sqlite3.connect("spese.db")
conn.execute("PRAGMA foreign_keys = ON")


# Creazione delle tabelle
def crea_tabelle():
    conn.execute("""
        CREATE TABLE IF NOT EXISTS categorie (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS spese (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            importo REAL NOT NULL CHECK (importo > 0),
            categoria_id INTEGER NOT NULL,
            descrizione TEXT,
            FOREIGN KEY (categoria_id) REFERENCES categorie(id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS budget (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mese TEXT NOT NULL,
            categoria_id INTEGER NOT NULL,
            importo REAL NOT NULL CHECK (importo > 0),
            UNIQUE (mese, categoria_id),
            FOREIGN KEY (categoria_id) REFERENCES categorie(id)
        )
    """)

    conn.commit()


# Modulo 1 - Gestione categorie
def gestione_categorie():
    print("\n--- GESTIONE CATEGORIE ---")

    nome = input("Inserisci il nome della categoria: ").strip()

    if nome == "":
        print("Errore: il nome non può essere vuoto.")
        return

    categoria = conn.execute(
        "SELECT id FROM categorie WHERE nome = ? COLLATE NOCASE",
        (nome,)
    ).fetchone()

    if categoria:
        print("La categoria esiste già.")
    else:
        conn.execute(
            "INSERT INTO categorie (nome) VALUES (?)",
            (nome,)
        )
        conn.commit()
        print("Categoria inserita correttamente.")


# Modulo 2 - Inserimento spesa
def inserisci_spesa():
    print("\n--- INSERIMENTO SPESA ---")

    data = input("Inserisci la data (YYYY-MM-DD): ").strip()

    try:
        datetime.strptime(data, "%Y-%m-%d")
        if len(data) != 10:
            raise ValueError
    except ValueError:
        print("Errore: data non valida.")
        return

    try:
        importo = float(input("Inserisci l'importo: ").replace(",", "."))
    except ValueError:
        print("Errore: inserisci un numero.")
        return

    if not 0 < importo < float("inf"):
        print("Errore: l'importo deve essere maggiore di zero.")
        return

    nome = input("Inserisci la categoria: ").strip()

    categoria = conn.execute(
        "SELECT id FROM categorie WHERE nome = ? COLLATE NOCASE",
        (nome,)
    ).fetchone()

    if categoria is None:
        print("Errore: la categoria non esiste.")
        return

    descrizione = input("Inserisci una descrizione (facoltativa): ")

    conn.execute("""
        INSERT INTO spese (data, importo, categoria_id, descrizione)
        VALUES (?, ?, ?, ?)
    """, (data, importo, categoria[0], descrizione))

    conn.commit()
    print("Spesa inserita correttamente.")


# Modulo 3 - Budget mensile
def imposta_budget():
    print("\n--- BUDGET MENSILE ---")

    mese = input("Inserisci il mese (YYYY-MM): ").strip()

    try:
        datetime.strptime(mese, "%Y-%m")
        if len(mese) != 7:
            raise ValueError
    except ValueError:
        print("Errore: mese non valido.")
        return

    nome = input("Inserisci la categoria: ").strip()

    try:
        importo = float(input("Inserisci il budget: ").replace(",", "."))
    except ValueError:
        print("Errore: inserisci un numero.")
        return

    if not 0 < importo < float("inf"):
        print("Errore: il budget deve essere maggiore di zero.")
        return

    categoria = conn.execute(
        "SELECT id FROM categorie WHERE nome = ? COLLATE NOCASE",
        (nome,)
    ).fetchone()

    if categoria is None:
        print("Errore: la categoria non esiste.")
        return

    budget = conn.execute("""
        SELECT id FROM budget
        WHERE mese = ? AND categoria_id = ?
    """, (mese, categoria[0])).fetchone()

    if budget:
        conn.execute("""
            UPDATE budget SET importo = ?
            WHERE id = ?
        """, (importo, budget[0]))
    else:
        conn.execute("""
            INSERT INTO budget (mese, categoria_id, importo)
            VALUES (?, ?, ?)
        """, (mese, categoria[0], importo))

    conn.commit()
    print("Budget mensile salvato correttamente.")


# Report 1 - Totale spese per categoria
def totale_spese():
    print("\n--- TOTALE SPESE PER CATEGORIA ---")

    risultati = conn.execute("""
        SELECT categorie.nome, SUM(spese.importo)
        FROM spese
        JOIN categorie ON spese.categoria_id = categorie.id
        GROUP BY categorie.id, categorie.nome
    """).fetchall()

    if not risultati:
        print("Non ci sono spese registrate.")

    for nome, totale in risultati:
        print(nome, "-", round(totale, 2), "euro")


# Report 2 - Spese mensili e budget
def confronto_budget():
    print("\n--- SPESE MENSILI VS BUDGET ---")

    mese = input("Inserisci il mese (YYYY-MM): ").strip()

    try:
        datetime.strptime(mese, "%Y-%m")
        if len(mese) != 7:
            raise ValueError
    except ValueError:
        print("Errore: mese non valido.")
        return

    risultati = conn.execute("""
        SELECT categorie.id, categorie.nome, budget.importo
        FROM budget
        JOIN categorie ON budget.categoria_id = categorie.id
        WHERE budget.mese = ?
    """, (mese,)).fetchall()

    if not risultati:
        print("Nessun budget presente per questo mese.")

    for categoria_id, nome, budget in risultati:

        speso = conn.execute("""
            SELECT SUM(importo)
            FROM spese
            WHERE categoria_id = ?
            AND substr(data, 1, 7) = ?
        """, (categoria_id, mese)).fetchone()[0]

        if speso is None:
            speso = 0

        print("\nMese:", mese)
        print("Categoria:", nome)
        print("Budget:", round(budget, 2), "euro")
        print("Speso:", round(speso, 2), "euro")

        if round(speso, 2) > round(budget, 2):
            print("Stato: SUPERAMENTO BUDGET")
        else:
            print("Stato: BUDGET RISPETTATO")


# Report 3 - Elenco delle spese
def elenco_spese():
    print("\n--- ELENCO COMPLETO DELLE SPESE ---")

    risultati = conn.execute("""
        SELECT spese.data, categorie.nome,
               spese.importo, spese.descrizione
        FROM spese
        JOIN categorie ON spese.categoria_id = categorie.id
        ORDER BY spese.data
    """).fetchall()

    if not risultati:
        print("Non ci sono spese registrate.")

    print("Data | Categoria | Importo | Descrizione")

    for data, nome, importo, descrizione in risultati:
        if descrizione is None:
            descrizione = ""

        print(data, "|", nome, "|", importo, "|", descrizione)


# Modulo 4 - Menu dei report
def menu_report():
    while True:
        print("\n--- MENU REPORT ---")
        print("1. Totale spese per categoria")
        print("2. Spese mensili vs budget")
        print("3. Elenco completo delle spese")
        print("4. Ritorna al menu principale")

        scelta = input("Inserisci la tua scelta: ")

        if scelta == "1":
            totale_spese()

        elif scelta == "2":
            confronto_budget()

        elif scelta == "3":
            elenco_spese()

        elif scelta == "4":
            break

        else:
            print("Scelta non valida. Riprovare.")


# Menu principale
def menu_principale():
    while True:
        print("\n-------------------------")
        print(" SISTEMA SPESE PERSONALI")
        print("-------------------------")
        print("1. Gestione Categorie")
        print("2. Inserisci Spesa")
        print("3. Definisci Budget Mensile")
        print("4. Visualizza Report")
        print("5. Esci")
        print("-------------------------")

        scelta = input("Inserisci la tua scelta: ")

        if scelta == "1":
            gestione_categorie()

        elif scelta == "2":
            inserisci_spesa()

        elif scelta == "3":
            imposta_budget()

        elif scelta == "4":
            menu_report()

        elif scelta == "5":
            print("Arrivederci!")
            break

        else:
            print("Scelta non valida. Riprovare.")


# Avvio del programma
crea_tabelle()

print("Benvenuto nel sistema di gestione delle spese personali!")

menu_principale()

conn.close()
