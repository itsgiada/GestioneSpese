# Sistema di gestione delle spese personali e del budget

## Descrizione

Il progetto permette di gestire le spese personali attraverso un programma Python collegato a un database SQLite.

## Funzionalità

- Inserimento delle categorie.
- Registrazione delle spese.
- Definizione del budget mensile.
- Visualizzazione del totale delle spese per categoria.
- Confronto tra spese mensili e budget.
- Visualizzazione delle spese ordinate per data.

## Requisiti

- Python 3
- Libreria standard sqlite3
- Libreria standard datetime

Non è necessario installare librerie aggiuntive.

## Istruzioni per l'esecuzione

1. Scaricare il progetto.
2. Aprire il terminale nella cartella del progetto.
3. Per caricare i dati di esempio in un database nuovo, eseguire il comando:

`python -c "import sqlite3; c=sqlite3.connect('spese.db'); c.executescript(open('sql/database.sql', encoding='utf-8').read()); c.commit(); c.close()"`

4. Avviare il programma con il comando:

`python main.py`

5. Selezionare una delle opzioni del menu.

Il comando per caricare i dati di esempio deve essere eseguito una sola volta.

## Database

Il database è composto da tre tabelle:

- categorie
- spese
- budget

Lo script SQL si trova nella cartella sql, nel file database.sql.