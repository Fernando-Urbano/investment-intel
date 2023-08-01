import os
import re
import sys
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta 
import zipfile
from django.utils import timezone
import pandas as pd
import numpy as np
import logging
from typing import Union
import sqlite3
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investmentintel.settings')
django.setup()

from fundsintel.models import InvestmentFund

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# fund = InvestmentFund.objects.get(cnpj='00.017.024/0001-53')
# data = fund.get_data(normalize=True)
# data

# def create_registration_info_table(data_path: str = "fundsintel") -> None:
#     conn = sqlite3.connect(data_path + "\\" + "funds_info.db")
#     cursor = conn.cursor()
#     cursor.execute(
#         '''
#         CREATE TABLE IF NOT EXISTS registration_info (
#             id INTEGER PRIMARY KEY,
#             cnpj VARCHAR(30),
#             fund_type VARCHAR(100),
#             name VARCHAR(200),
#             dt_registration DATE,
#             dt_establishment DATE,
#             dt_cancel DATE,
#             cd_cvm INT,
#             situation VARCHAR(100),
#             dt_situation DATE,
#             dt_exerc_start DATE,
#             dt_exerc_end DATE,
#             class_cvm VARCHAR(100),
#             dt_class_cvm DATE,
#             dt_act_start DATE,
#             profitability VARCHAR(100),
#             condominium_type VARCHAR(50),
#             divided_in_quotas BOOL,
#             exclusive BOOL,
#             long_term_taxation BOOL,
#             target_audience VARCHAR(50),
#             ent_invest BOOL,
#             performance_fee REAL,
#             information_performance_fee VARCHAR(300),
#             adm_fee REAL,
#             information_adm_fee VARCHAR(300),
#             net_equity REAL,
#             dt_net_equity DATE,
#             director VARCHAR(150),
#             cnpj_adm VARCHAR(30),
#             adm VARCHAR(100),
#             pf_pj_manager VARCHAR(10),
#             cpf_cnpj_manager VARCHAR(30),
#             manager VARCHAR(150),
#             cnpj_auditor VARCHAR(30),
#             auditor VARCHAR(150),
#             cnpj_custodian VARCHAR(150),
#             custodian VARCHAR(150),
#             cnpj_controler VARCHAR(150),
#             controler VARCHAR(150),
#             authorized_to_invest_all_offshore BOOL,
#             class_anbima VARCHAR(100),
#             dt_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#         );
#         '''
#     )
#     conn.commit()


registration_info_dtypes = {
    'TP_FUNDO': 'object',
    'CNPJ_FUNDO': 'object',
    'DENOM_SOCIAL': 'object',
    'DT_REG': 'object',
    'DT_CONST': 'object',
    'CD_CVM': 'float64',
    'DT_CANCEL': 'object',
    'SIT': 'object',
    'DT_INI_SIT': 'object',
    'DT_INI_ATIV': 'object',
    'DT_INI_EXERC': 'object',
    'DT_FIM_EXERC': 'object',
    'CLASSE': 'object',
    'DT_INI_CLASSE': 'object',
    'RENTAB_FUNDO': 'object',
    'CONDOM': 'object',
    'FUNDO_COTAS': 'object',
    'FUNDO_EXCLUSIVO': 'object',
    'TRIB_LPRAZO': 'object',
    'PUBLICO_ALVO': 'object',
    'ENTID_INVEST': 'object',
    'TAXA_PERFM': 'float64',
    'INF_TAXA_PERFM': 'object',
    'TAXA_ADM': 'float64',
    'INF_TAXA_ADM': 'object',
    'VL_PATRIM_LIQ': 'float64',
    'DT_PATRIM_LIQ': 'object',
    'DIRETOR': 'object',
    'CNPJ_ADMIN': 'object',
    'ADMIN': 'object',
    'PF_PJ_GESTOR': 'object',
    'CPF_CNPJ_GESTOR': 'object',
    'GESTOR': 'object',
    'CNPJ_AUDITOR': 'object',
    'AUDITOR': 'object',
    'CNPJ_CUSTODIANTE': 'object',
    'CUSTODIANTE': 'object',
    'CNPJ_CONTROLADOR': 'object',
    'CONTROLADOR': 'object',
    'INVEST_CEMPR_EXTER': 'object',
    'CLASSE_ANBIMA': 'object'
}

registration_info_attr = {
    'CNPJ_FUNDO': 'cnpj',
    'TP_FUNDO': 'fund_type',
    'DENOM_SOCIAL': 'name',
    'DT_REG': 'dt_registration',
    'DT_CONST': 'dt_establishment',
    'CD_CVM': 'cd_cvm',
    'SIT': 'situation',
    'DT_INI_SIT': 'dt_situation',
    'DT_INI_ATIV': 'dt_act_start',
    'DT_INI_EXERC': 'dt_exerc_start',
    'DT_FIM_EXERC': 'dt_exerc_end',
    'CLASSE': 'class_cvm',
    'DT_INI_CLASSE': 'dt_class_cvm',
    'DT_CANCEL': 'dt_cancel',
    'RENTAB_FUNDO': 'profitability',
    'CONDOM': 'condominium_type',
    'FUNDO_COTAS': 'divided_in_quotas',
    'FUNDO_EXCLUSIVO': 'exclusive',
    'TRIB_LPRAZO': 'long_term_taxation',
    'PUBLICO_ALVO': 'target_audience',
    'ENTID_INVEST': 'ent_invest',
    'TAXA_PERFM': 'performance_fee',
    'INF_TAXA_PERFM': 'performance_fee_information',
    'TAXA_ADM': 'adm_fee',
    'INF_TAXA_ADM': 'adm_fee_information',
    'VL_PATRIM_LIQ': 'net_equity',
    'DT_PATRIM_LIQ': 'dt_net_equity',
    'DIRETOR': 'director',
    'CNPJ_ADMIN': 'cnpj_adm',
    'ADMIN': 'adm',
    'PF_PJ_GESTOR': 'manager_pf_pj',
    'CPF_CNPJ_GESTOR': 'manager_cpf_cnpj',
    'GESTOR': 'manager',
    'CNPJ_AUDITOR': 'auditor_cnpj',
    'AUDITOR': 'auditor',
    'CNPJ_CUSTODIANTE': 'custodian_cnpj',
    'CUSTODIANTE': 'custodian',
    'CNPJ_CONTROLADOR': 'controler_cnpj',
    'CONTROLADOR': 'controler',
    'INVEST_CEMPR_EXTER': 'authorized_to_invest_all_offshore',
    'CLASSE_ANBIMA': 'class_anbima'
}


def transform_registration_info_to_sql(
    raw_data_path: str = "fundsintel\\funds_data_routine\\raw_data",
    force_update: bool = False
) -> None:
    fund_last_updated = InvestmentFund.objects.latest('dt_updated')
    registration_info = pd.read_csv(
        raw_data_path + "\\" + "cad_fi.csv", encoding='latin1', sep=";",
        dtype=registration_info_dtypes
    )
    registration_info.rename(registration_info_attr, axis=1, inplace=True)
    bool_columns = [
        'divided_in_quotas', 'exclusive', 'long_term_taxation', 'ent_invest',
        'authorized_to_invest_all_offshore'
    ]
    registration_info[bool_columns] = registration_info[bool_columns].replace({"S": True, "N": False})
    dt_columns = registration_info.filter(regex=r'^dt_').columns
    registration_info[dt_columns] = registration_info[dt_columns].apply(pd.to_datetime, errors='coerce')
    registration_info[dt_columns] = registration_info[dt_columns].replace({pd.NaT: None})
    registration_info.replace({np.nan: None}, inplace=True)
    registration_info.sort_values(['cnpj', 'dt_situation'], ascending=[True, False], inplace=True)
    registration_info_records = registration_info.to_dict(orient='records')
    funds_added, funds_updated = 0, 0
    for record in registration_info_records:
        if InvestmentFund.objects.filter(cnpj=record['cnpj']).exists():
            fund = InvestmentFund.objects.get(cnpj=record['cnpj'])
            fund.__dict__.update(**record)
            fund.save()
            funds_updated += 1
            logging.info(f"Updated {fund.cnpj}, totalizing {funds_updated} updated funds")
        else:
            fund = InvestmentFund(**record)
            fund.save()
            funds_added += 1
            logging.info(f"Added {fund.cnpj}, totalizing {funds_added} new funds")