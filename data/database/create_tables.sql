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
    noticia_id INTEGER PRIMARY KEY,
    titulo TEXT,
    url TEXT NOT NULL UNIQUE,
    lead TEXT,
    data_hora TEXT, 
);

CREATE TABLE IF NOT EXISTS pipeline_metadata (
    key TEXT PRIMARY KEY,
    value TEXT
);
