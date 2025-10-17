import pandas as pd
import hashlib
from urllib.parse import urlparse


class Transform:
    def __init__(self):
        self.removed_news = pd.DataFrame()
        self.removed_yahoo = pd.DataFrame()

    def clean_news(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            self.removed_news = pd.DataFrame()
            return df

        df_valid = df[df["url"].apply(self._is_valid_url)]
        self.removed_news = df[~df.index.isin(df_valid.index)].copy()

        df_valid["url_hash"] = df_valid["url"].apply(
            lambda x: hashlib.md5(x.encode("utf-8")).hexdigest()
        )

        duplicates = df_valid[
            df_valid.duplicated(subset=["url_hash"], keep="first")
        ].copy()
        self.removed_news = pd.concat(
            [self.removed_news, duplicates], ignore_index=True
        )

        df_clean = df_valid.drop_duplicates(subset=["url_hash"]).reset_index(drop=True)

        def format_datetime_br(dt_str):
            try:
                dt = pd.to_datetime(dt_str)
                return dt.strftime("%d/%m/%y %H:%M:%S")
            except:
                return "Sem dados"

        df_clean["dataHora"] = df_clean["dataHora"].apply(format_datetime_br)

        df_clean = df_clean.fillna("Sem dados")
        df_clean = df_clean.replace(r"^\s*$", "Sem dados", regex=True)

        df_clean = df_clean.drop(columns=["url_hash"])
        return df_clean

    def clean_yahoo(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            self.removed_yahoo = pd.DataFrame()
            return df

        df_clean = df.copy()

        df_clean["Date"] = pd.to_datetime(df_clean["Date"], errors="coerce")
        df_clean = df_clean.dropna(subset=["Date"], how="all")
        df_clean["Date"] = df_clean["Date"].apply(
            lambda x: x.strftime("%d/%m/%y") if pd.notnull(x) else "Sem dados"
        )

        if "Data_Coletada" in df_clean.columns:
            df_clean["Data_Coletada"] = pd.to_datetime(
                df_clean["Data_Coletada"], errors="coerce"
            )
            df_clean["Data_Coletada"] = df_clean["Data_Coletada"].apply(
                lambda x: x.strftime("%d/%m/%y") if pd.notnull(x) else "Sem dados"
            )

        numeric_cols = ["Open", "High", "Low", "Close", "Volume"]
        for col in numeric_cols:
            if col in df_clean.columns:
                df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")
                df_clean[col] = df_clean[col].fillna("Sem dados")

        df_clean["hash"] = (
            df_clean["Date"].astype(str) + df_clean["ticker"].astype(str)
        ).apply(lambda x: hashlib.md5(x.encode("utf-8")).hexdigest())

        duplicates = df_clean[df_clean.duplicated(subset=["hash"], keep="first")].copy()
        self.removed_yahoo = duplicates.copy()

        df_clean = df_clean.drop_duplicates(subset=["hash"]).reset_index(drop=True)
        df_clean = df_clean.drop(columns=["hash"])

        if not df_clean.empty:
            df_clean = self._filter_last_6_months(df_clean)

        df_clean = df_clean.fillna("Sem dados")
        df_clean = df_clean.replace(r"^\s*$", "Sem dados", regex=True)

        return df_clean

    def _is_valid_url(self, url: str) -> bool:
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False

    def _filter_last_6_months(self, df: pd.DataFrame) -> pd.DataFrame:
        df_copy = df.copy()
        df_copy["Date_dt"] = pd.to_datetime(
            df_copy["Date"], format="%d/%m/%y", errors="coerce"
        )
        last_date = df_copy["Date_dt"].max()
        six_months_ago = last_date - pd.DateOffset(months=6)
        df_6m = df_copy[df_copy["Date_dt"] >= six_months_ago].copy()
        df_6m = df_6m.drop(columns=["Date_dt"])
        return df_6m
