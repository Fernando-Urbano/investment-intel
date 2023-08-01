import os
import re  # Rename this variable to avoid conflict with module
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta 
import zipfile
import pandas as pd
import logging
from typing import Union
import sqlite3

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
os.environ['PYDEVD_WARN_EVALUATION_TIMEOUT'] = '30'

def create_daily_info_table(data_path: str = "fundsintel") -> None:
    conn = sqlite3.connect(data_path + "\\" + "funds_info.db")
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS daily_info (
            id INTEGER PRIMARY KEY,
            cnpj VARCHAR(30),
            dt_comptc DATE,
            quota REAL,
            value REAL,
            net_equity REAL,
            raise_value REAL,
            rescue_value REAL,
            shareholders INT,
            dt_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    conn.commit()


def transform_daily_info_to_sql(
    data_path: str = "fundsintel",
    raw_data_path: str = "fundsintel\\funds_data_routine\\raw_data",
    first_dt_comptc: Union[date, datetime, None] = None
) -> None:
    conn = sqlite3.connect(data_path + "\\" + "funds_info.db")
    cursor = conn.cursor()
    funds_info_monthly_files = {
        datetime.strptime(re.search("([0-9]{6})[.]csv", f).group(1) + "01", "%Y%m%d").date(): f
        for f in os.listdir(raw_data_path) if re.search("inf_diario_fi_[0-9]{6}[.]csv", f)
    }
    if first_dt_comptc:
        funds_info_monthly_files = {dt: f for dt, f in funds_info_monthly_files.items() if dt >= first_dt_comptc}
    if not funds_info_monthly_files:
        logging.info(f"No monthly files found")
        return None
    cursor.execute(f"DELETE FROM daily_info WHERE dt_comptc >= '{first_dt_comptc.strftime('%Y-%m-%d')}'")
    conn.commit()
    for monthly_file in funds_info_monthly_files.values():
        monthly_info = pd.read_csv(raw_data_path + "\\" + monthly_file, sep=";", dtype={
            "TP_FUNDO": "object",
            "CNPJ_FUNDO": "object",
            "DT_COMPTC": "object",
            "VL_TOTAL": "float",
            "VL_QUOTA": "float",
            "VL_PATRIM_LIQ": "float",
            "CAPTC_DIA": "float",
            "RESG_DIA": "float",
            "NR_COTST": "float",
        })
        monthly_info.rename({
            "TP_FUNDO": "fund_type",
            "CNPJ_FUNDO": "cnpj",
            "DT_COMPTC": "dt_comptc",
            "VL_TOTAL": "value",
            "VL_QUOTA": "quota",
            "VL_PATRIM_LIQ": "net_equity",
            "CAPTC_DIA": "raise_value",
            "RESG_DIA": "rescue_value",
            "NR_COTST": "shareholders",
        }, axis=1, inplace=True)
        if 'fund_type' in list(monthly_info.columns):
            monthly_info.drop("fund_type", axis=1, inplace=True)
        monthly_info.to_sql('daily_info', conn, if_exists='append', index=False)
        conn.commit()
        logging.info(f"Added daily information from '{monthly_file}' to 'daily_info' table")
        # os.remove(raw_data_path + "\\" + monthly_file)
    logging.info(f"Finished 'funds_quota' data update")