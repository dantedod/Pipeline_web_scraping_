# src/extract_news.py
from src.task import Task
import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from datetime import datetime


class ExtractNews(Task):
    def __init__(self, urls):
        super().__init__("ExtractNews")
        self.urls_g1 = urls.get("g1", [])
        self.urls_folha = urls.get("folha", [])

    def execute(self, data=None):
        noticias = []
        count = 0
        logger = logging.getLogger("ExtractNews")

        def coletar_g1(url_base):
            nonlocal count
            try:
                logger.info(f"Coletando G1: {url_base}")
                res = requests.get(url_base, timeout=5)
                res.raise_for_status()
                soup = BeautifulSoup(res.text, "html.parser")
                blocos = soup.find_all("div", class_="bastian-feed-item")
                for bloco in blocos:
                    a_tag = bloco.find("a", href=True)
                    if not a_tag or not a_tag.get("href"):
                        continue
                    count += 1
                    url = a_tag.get("href")
                    res_noticia = requests.get(url, timeout=5)
                    soup_noticia = BeautifulSoup(res_noticia.text, "html.parser")
                    lead_tag = soup_noticia.find("p", class_="content-text__container")
                    time_tag = soup_noticia.find("time")
                    noticias.append(
                        {
                            "NoticiaID": count,
                            "titulo": a_tag.text.strip(),
                            "url": url,
                            "lead": lead_tag.text.strip() if lead_tag else "",
                            "dataHora": time_tag["datetime"] if time_tag else "",
                        }
                    )
            except Exception as e:
                logger.error(f"Erro G1: {url_base} - {e}")

        def coletar_folha(url_base):
            nonlocal count
            try:
                logger.info(f"Coletando Folha: {url_base}")
                res = requests.get(url_base, timeout=5)
                res.raise_for_status()
                soup = BeautifulSoup(res.text, "html.parser")
                blocos = soup.select("ol.u-list-unstyled li.c-headline")
                for bloco in blocos:
                    a_tag = bloco.find("a", href=True)
                    if not a_tag:
                        continue
                    count += 1
                    url = a_tag["href"]
                    titulo_tag = bloco.find("h2", class_="c-headline__title")
                    lead_tag = bloco.find("p", class_="c-headline__standfirst")
                    time_tag = bloco.find("time")
                    noticias.append(
                        {
                            "NoticiaID": count,
                            "titulo": titulo_tag.text.strip() if titulo_tag else "",
                            "url": url,
                            "lead": lead_tag.text.strip() if lead_tag else "",
                            "dataHora": time_tag["datetime"] if time_tag else "",
                        }
                    )
            except Exception as e:
                logger.error(f"Erro Folha: {url_base} - {e}")

        for url in self.urls_g1:
            coletar_g1(url)
        for url in self.urls_folha:
            coletar_folha(url)

        return pd.DataFrame(noticias)
