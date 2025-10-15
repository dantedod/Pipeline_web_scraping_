import os
import sqlite3


def init_db(db_path="../data/database/pipeline.db", schema_file=None):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.executescript(
        """
    PRAGMA foreign_keys = ON;

    CREATE TABLE IF NOT EXISTS instruments (
        instrument_id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker TEXT NOT NULL UNIQUE,
        nome TEXT,
        setor TEXT,
        pais TEXT,
        bolsa TEXT
    );

    CREATE TABLE IF NOT EXISTS prices (
        date TEXT NOT NULL,
        ticker TEXT NOT NULL,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        volume INTEGER,
        data_coletada TEXT,
        PRIMARY KEY (date, ticker),
        FOREIGN KEY (ticker) REFERENCES instruments(ticker) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        noticia_id INTEGER,
        titulo TEXT,
        url TEXT NOT NULL UNIQUE,
        lead TEXT,
        data_hora TEXT
    );

    CREATE TABLE IF NOT EXISTS pipeline_metadata (
        key TEXT PRIMARY KEY,
        value TEXT
    );
    """
    )
    conn.commit()
    conn.close()
    print("✅ Banco inicializado em:", db_path)


if __name__ == "__main__":
    init_db()
