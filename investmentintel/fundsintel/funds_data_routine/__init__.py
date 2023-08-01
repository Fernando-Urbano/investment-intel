from download_data import download_funds_info
from organize_registration_info import transform_registration_info_to_sql
from organize_daily_info import create_daily_info_table, transform_daily_info_to_sql
from datetime import date
from dateutil.relativedelta import relativedelta
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

funds_registration_info = {'download': False, 'update': False}
funds_daily_info = {'download': False, 'update': False}
funds_old_daily_info = {'download': False, 'update': True}

# Funds Registration Information
if funds_registration_info['download']:
    download_funds_info(
        url_raw="http://dados.cvm.gov.br/dados/FI/CAD/DADOS/",
    )
if funds_registration_info['update']:
    transform_registration_info_to_sql()

# Daily Reports
start_dt_comptc = (date.today() - relativedelta(months=48)).replace(day=1)
if funds_daily_info['download']:
    download_funds_info(
        url_raw="http://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/",
        first_dt_comptc=start_dt_comptc
    )
if funds_daily_info['update']:
    create_daily_info_table()
    transform_daily_info_to_sql(first_dt_comptc=start_dt_comptc)

# Old Daily Reports
start_year = 2018
if funds_old_daily_info['download']:
    download_funds_info(
        url_raw="http://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/HIST/",
        first_year=start_year
    )
if funds_old_daily_info['update']:
    create_daily_info_table()
    transform_daily_info_to_sql(first_dt_comptc=date(year=start_year, month=1, day=1))