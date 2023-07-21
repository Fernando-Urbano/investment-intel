from download_data import download_funds_info
from organize_registration_info import transform_registration_info_to_sql
from organize_daily_info import create_daily_info_table, transform_daily_info_to_sql
from datetime import date
from dateutil.relativedelta import relativedelta
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Funds Registration Information
download_funds_info(
    url_raw="http://dados.cvm.gov.br/dados/FI/CAD/DADOS/",
)
transform_registration_info_to_sql()

# Daily Reports
start_dt_comptc = (date.today() - relativedelta(months=2)).replace(day=1)
download_funds_info(
    url_raw="http://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/",
    first_dt_comptc=start_dt_comptc
)
create_daily_info_table()
transform_daily_info_to_sql(first_dt_comptc=start_dt_comptc)