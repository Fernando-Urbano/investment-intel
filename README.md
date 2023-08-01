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

# Files
## funds_data_routine
### funds_data_routine/download_data.py
This file has the connection with the CVM website using `BeautifulSoup`.

### funds_data_routine/organize_daily_info.py
This file creates the SQLite table for daily_info and puts the data from csv files into it. It always delete past data before adding new ones.

### funds_data_routine/organize_registration_info.py
This file adds data to the `InvestmentFund` django model. If a certain fund already has data, the file will update the fund's data steady of adding another model.

## models.py
Contains the django models `InvestmentFund` and `User`. With `get_data` method, it allows us to get data of a specific fund and with the `short_name` property we can show the name of the fund in a shorter way.

## views.py
### views.py > index
`index` function inside of views.py redirects the user to the main page of the application. The application works with only one page, but allows the user to view multiple funds due to React and the concept of SPA (Single Page Application).

### views.py > search_market_data
Returns up to 10 funds that have the characters specified in the parameter "query". It called everytime the user writes a name inside of the search bar. In this way, the user can view the options he can select that most look like the funds he/she is searching.

```
@csrf_exempt
def search_market_data(request):
    data = json.loads(request.body)
    query = data.get("query")
    query_results = InvestmentFund.objects.filter(Q(name__icontains=query))[:10]
    return JsonResponse({"query_results": [q.serialize() for q in query_results]}, safe=False)
```

### views.py > get_market_data
The function `get_market_data` allows the user to get daily info on quota, returns, number of investors, AUM, and other specifications of the selected hedge funds.

It has the following parameters:
- `cnpjs`: the id for each of the hedge funds.
- `data_type`: which kind of data is wanted.
- `period`: selected period of search (i.e. 1 month, 3 months, YTD). When the `period` is selected the `start_dt_comptc` and the `end_dt_comptc` are automatically specified as well.
- `start_dt_comptc`: start date of the query.
- `end_dt_comptc`: end date of the query.
