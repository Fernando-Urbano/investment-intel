import os
import re
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta 
import zipfile
import pandas as pd
import logging
import sqlite3

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
os.environ['PYDEVD_WARN_EVALUATION_TIMEOUT'] = '30'


def download_funds_info(
    url_raw,
    raw_data_path="fundsintel\\funds_data_routine\\raw_data",
    first_dt_comptc=None,
    first_year=None
):
    current_dir = os.getcwd()
    if raw_data_path:
        os.chdir(raw_data_path)
    response = requests.get(url_raw)
    soup = BeautifulSoup(response.text, "html.parser")
    links = [a["href"] for a in soup.find_all("a")]
    zip_csv_links = [link for link in links if re.search(r'\.(csv|zip)$', link)]
    
    if first_dt_comptc:
        if isinstance(first_dt_comptc, str):
            first_dt_comptc = datetime.strptime(first_dt_comptc, "%Y-%m-%d").date()
        selected_folders = [
            d.strftime("%Y%m") for d
            in pd.date_range(start=first_dt_comptc, end=datetime.now().date(), freq='MS')
        ]
        zip_csv_links = [l for l in zip_csv_links if any(folder in l for folder in selected_folders)]

    if first_year:
        first_year = int(first_year)
        selected_folders = [str(d) for d in range(first_year, date.today().year + 1, 1)]
        zip_csv_links = [l for l in zip_csv_links if any(folder in l for folder in selected_folders)]
    
    current_file_number = 0
    number_files = len(zip_csv_links)
    logging.info(f"Found {number_files} files of funds daily information")
    for new_link in zip_csv_links:
        current_file_number += 1
        download_link = urljoin(url_raw, new_link)
        file_name = os.path.basename(new_link)
        with open(file_name, 'wb') as file:
            response = requests.get(download_link)
            file.write(response.content)
        logging.info(f"Downloaded file: {file_name} ({current_file_number}/{number_files})")
    
    zip_files = [file for file in os.listdir() if file.endswith(".zip")]

    for zip_file in zip_files:
        try:
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall()
            os.remove(zip_file)
            logging.info(f"Unziped {zip_file}")
        except Exception as e:
            logging.error(f"Error in {zip_file}: {e}")

    os.chdir(current_dir)
