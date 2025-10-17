import os
import sqlite3
import pandas as pd
from typing import Tuple


class Load:
    def __init__(self, db_path="../data/analytcs/pipeline.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def save_news(self, df: pd.DataFrame) -> Tuple[int, int]:
        if df is None or df.empty:
            return 0, 0

        df = df.copy()
        df = df.rename(
            columns={
                "NoticiaID": "noticia_id",
                "NoticiaId": "noticia_id",
                "title": "titulo",
                "link": "url",
                "summary": "lead",
                "dataHora": "data_hora",
                "published_at": "data_hora",
            }
        )

        cols_expected = ["noticia_id", "titulo", "url", "lead", "data_hora"]
        for c in cols_expected:
            if c not in df.columns:
                df[c] = None

        records = df[cols_expected].values.tolist()

        insert_sql = """
        INSERT OR IGNORE INTO news (noticia_id, titulo, url, lead, data_hora)
        VALUES (?, ?, ?, ?, ?)
        """

        with self._connect() as conn:
            cur = conn.cursor()
            before = cur.execute("SELECT COUNT(1) FROM news").fetchone()[0]
            cur.executemany(insert_sql, records)
            conn.commit()
            after = cur.execute("SELECT COUNT(1) FROM news").fetchone()[0]

        inserted = max(0, after - before)
        ignored = max(0, len(records) - inserted)
        return inserted, ignored

    def save_instruments(self, df: pd.DataFrame) -> Tuple[int, int]:
        if df is None or df.empty:
            return 0, 0

        df = df.copy()
        df = df.rename(
            columns={
                "Ticker": "ticker",
                "Nome": "nome",
                "Setor": "setor",
                "Pais": "pais",
                "Bolsa": "bolsa",
            }
        )

        if "ticker" not in df.columns or df["ticker"].isnull().all():
            if "symbol" in df.columns:  # Yahoo Finance normalmente traz o código aqui
                df["ticker"] = df["symbol"]
            elif "Ticker" in df.columns:
                df["ticker"] = df["Ticker"]
            elif "nome" in df.columns:
                df["ticker"] = df["nome"]
            else:
                df["ticker"] = "DESCONHECIDO"

        if "nome" not in df.columns or df["nome"].isnull().all():
            if "Empresa" in df.columns:
                df["nome"] = df["Empresa"]
            else:
                df["nome"] = df["ticker"]

        cols_expected = ["ticker", "nome", "setor", "pais", "bolsa"]
        for c in cols_expected:
            if c not in df.columns:
                df[c] = None

        records = df[cols_expected].drop_duplicates(subset=["ticker"]).values.tolist()

        insert_sql = """
        INSERT OR IGNORE INTO instruments (ticker, nome, setor, pais, bolsa)
        VALUES (?, ?, ?, ?, ?)
        """

        with self._connect() as conn:
            cur = conn.cursor()
            before = cur.execute("SELECT COUNT(1) FROM instruments").fetchone()[0]
            cur.executemany(insert_sql, records)
            conn.commit()
            after = cur.execute("SELECT COUNT(1) FROM instruments").fetchone()[0]

        inserted = max(0, after - before)
        ignored = max(0, len(records) - inserted)
        return inserted, ignored

    def save_prices(self, df: pd.DataFrame) -> Tuple[int, int]:
        if df is None or df.empty:
            return 0, 0

        df = df.copy()

        df = df.rename(
            columns={
                "date": "Date",
                "data_coletada": "Data_Coletada",
            }
        )

        cols_expected = [
            "Date",
            "ticker",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
            "Data_Coletada",
        ]
        for c in cols_expected:
            if c not in df.columns:
                df[c] = None

        def normalize_date(v):
            if pd.isna(v):
                return None
            try:
                d = pd.to_datetime(str(v), dayfirst=True, errors="coerce")
                if pd.isna(d):
                    d = pd.to_datetime(str(v), errors="coerce")
                if pd.isna(d):
                    return None
                return d.strftime("%Y-%m-%d")
            except:
                return None

        df["Date"] = df["Date"].apply(normalize_date)
        df = df[df["Date"].notna() & df["ticker"].notna()].copy()

        for num in ["Open", "High", "Low", "Close", "Volume"]:
            df[num] = pd.to_numeric(df[num], errors="coerce")

        records = df[
            [
                "Date",
                "ticker",
                "Open",
                "High",
                "Low",
                "Close",
                "Volume",
                "Data_Coletada",
            ]
        ].values.tolist()

        upsert_sql = """
      INSERT OR REPLACE INTO prices (date, ticker, open, high, low, close, volume, data_coletada)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
      """

        with self._connect() as conn:
            cur = conn.cursor()
            cur.executemany(upsert_sql, records)
            conn.commit()
            attempted = len(records)

        return attempted, attempted

    def show_tables(self):
        with self._connect() as conn:
            df = pd.read_sql_query(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;", conn
            )
        return df
