# Investment Intel
This is the final project of the CS50 Web Development course with Django and JavaScript lectured by Harvard CS department.

# What is it?
This software is the MVP of a investment information provider for brazilian financial markets. The MVP contains registration and performance data of brazilians hedge funds and enables the user to analyze and compare the performance of any of the brazilian hedge funds registered in the CVM (brazilian agency responsible for hedge funds). 

# How to run the application
1) Clone the repository to your local machine in the desired folder.
```
git clone https://github.com/Fernando-Urbano/investment-intel.git
```
2) Enter inside the django project.
```
cd investment intel
```
3) Run fundsintel/funds_data_routine/__init__.py. This part will collect all the data from CVM website with `BeautifulSoup` package. The routine will download the registration files and transform them into objects of django model `InvestmentFund`, and add information of daily quota to the `daily_info` SQLite table (which is not a Django model). If you want to get only more recent data, you can change the `__init__.py` file to not download and not update the `funds_old_daily_info` as following:
```
# from this:
funds_registration_info = {'download': True, 'update': True}
funds_daily_info = {'download': True, 'update': True}
funds_old_daily_info = {'download': True, 'update': True}

# to this:
funds_registration_info = {'download': True, 'update': True}
funds_daily_info = {'download': True, 'update': True}
funds_old_daily_info = {'download': False, 'update': False}
```
```
python fundsintel/funds_data_routine/__init__.py
```
4) Run the django project and open the localhost:
```
python manage.py runserver
```
