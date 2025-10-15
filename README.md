# 📈 Pipeline de Web Scraping para Análise Financeira

Este projeto é uma pipeline automatizada que coleta, processa e armazena dados financeiros históricos de ações e notícias. O objetivo é mostrar minhas habilidades em web scraping, API pública, manipulação de dados e integração com banco de dados.

## 🔍 Descrição

A pipeline realiza as seguintes etapas:

1. **Extração de Dados**
   - **Notícias**: Coleta notícias financeiras de fontes como G1 e Folha de São Paulo.
   - **Dados Históricos**: Obtém séries temporais de ações utilizando a API pública do Yahoo Finance (`yfinance`).

2. **Processamento e Limpeza**
   - Deduplicação de registros.
   - Normalização de datas e valores numéricos.
   - Remoção de URLs inválidas ou duplicadas.

3. **Armazenamento**
   - Dados limpos são salvos em um banco SQLite local (`pipeline.db`).

## ⚙️ Tecnologias Utilizadas

- Python 3.9+
- `pandas` para manipulação de dados
- `requests` e `BeautifulSoup` para scraping de notícias
- `selenium` e `webdriver_manager` para scraping de páginas dinâmicas
- `yfinance` para dados históricos de ações
- SQLite para armazenamento local
- Logging com `logging` do Python

## 📂 Estrutura do Projeto

```bash
pipeline_web_scraping/
│
├─ src/
│ ├─ extract_news.py # Extração de notícias
│ ├─ extract_yahoo.py # Extração de dados históricos via Yahoo Finance
│ ├─ transform.py # Limpeza e transformação dos dados
│ ├─ load.py # Persistência no banco SQLite
│ ├─ pipeline.py # Execução da pipeline
│ ├─ task.py # Classe base para tarefas
| ├─init_db.py
│ └─ logger_config.py # Configuração de logs
│
├─ data/
│ ├─ raw/ # Dados brutos coletados
│ ├─ processed/ # Dados limpos e processados
│ └─ database/ # Banco SQLite
├─notbooks
  ├─main.ipynb # Script principal da pipeline
```


## 🚀 Como Executar

 Clone o repositório:

```bash
git clone https://github.com/dantedod/Pipeline_web_scraping_.git
cd Pipeline_web_scraping
````
Criar ambiente virtual
```bash
# Criar
python -m venv .venv
Windows (cmd):
.venv\Scripts\activate
# Ativar (macOS/Linux)
source .venv/bin/activate
```
Instale as dependências:
```bash
pip install -r requirements.txt
```
Inicie o Jupyer e execute o pipeline
```bash
jupyter notebook
```
Ou apenas rode manualmente no arquivo main.ipynb

## Autor
[Dante Dantas](https://www.linkedin.com/in/dantedod/) – Trabalho de portfólio e demonstração de habilidades em Python, Web Scraping e Engenharia de Dados.
