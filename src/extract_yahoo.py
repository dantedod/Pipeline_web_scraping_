# src/extract_yahoo.py
from src.task import Task
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import yfinance as yf
import pandas as pd
import logging
from datetime import datetime


class ExtractYahoo(Task):
    def __init__(self, url, tickers=None):
        super().__init__("ExtractYahoo")
        self.url = url
        self.tickers = tickers or []

    def execute(self, data=None):
        logger = logging.getLogger("ExtractYahoo")
        nomes = []
        valores_historicos = []

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        try:
            logger.info(f"Acessando {self.url}")
            driver.get(self.url)
            top_10_holding = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "section[data-testid='top-holdings']")
                )
            )
            nomes_tabela = top_10_holding.find_elements(
                By.XPATH, ".//div[.//a]//a//div//span"
            )
            for nome in nomes_tabela:
                ticker = nome.text.strip()
                if ticker:
                    nomes.append({"Nome": ticker})
            logger.info(f"Top 10 Holdings: {[n['Nome'] for n in nomes]}")
        except Exception as e:
            logger.error(f"Erro ao coletar top holdings: {e}")
        finally:
            driver.quit()
            logger.info("Driver do Selenium fechado.")

        data_coletada = datetime.now().strftime("%d/%m/%y %H:%M:%S")
        for ticker in nomes:
            ticker_nome = ticker["Nome"]
            try:
                acao = yf.Ticker(ticker_nome)
                historico_df = acao.history(period="6mo").reset_index()
                historico_df["Date"] = historico_df["Date"].dt.strftime("%Y-%m-%d")
                historico_df["ticker"] = ticker_nome
                historico_df["Empresa"] = acao.info.get("shortName", "N/A")
                historico_df["Setor"] = acao.info.get("sector", "N/A")
                historico_df["Industria"] = acao.info.get("industry", "N/A")
                historico_df["Moeda"] = acao.info.get("currency", "N/A")
                historico_df["Pais"] = acao.info.get("country", "N/A")
                historico_df["Bolsa"] = acao.info.get("exchange", "N/A")
                historico_df["Data_Coletada"] = data_coletada
                valores_historicos.append(historico_df)
            except Exception as e:
                logger.warning(f"Falha ao coletar {ticker_nome}: {e}")

        if valores_historicos:
            return pd.concat(valores_historicos, ignore_index=True)
        return pd.DataFrame()
