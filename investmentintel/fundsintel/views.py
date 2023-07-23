from django.shortcuts import render
from django.db import IntegrityError
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import logging
import json
import pandas as pd
import sqlite3
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

from .models import User, InvestmentFund

# Index page
def index(request):
    user = request.user
    return render(request, "fundsintel/index.html", {
        "user": user,
    })

# Register
def register(request):
    if request.method == "POST":
        # Get data
        first_name = request.POST["first_name"]
        surname = request.POST["surname"]
        username = request.POST["username"]
        email = request.POST["email"]
        user_info = f"{first_name} {surname} ({username} - {email})"
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            logging.info(f"User failed to match password when registering: {user_info}")
            return render(request, "register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.first_name = first_name
            user.surname = surname
            user.save()
        except IntegrityError:
            logging.info(f"User tried to use a username already taken: {user_info}")
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        logging.info(f"User successfully registered: {user_info}")
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    

# Login
def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username_or_email = request.POST["username_or_email"]
        password = request.POST["password"]
        user = authenticate(request, username=username_or_email, password=password)
        if user is None:
            user = authenticate(request, email=username_or_email, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            logging.info(f"User {username_or_email} successfully logged in")
            return HttpResponseRedirect(reverse("index"))
        else:
            logging.info(f"User {username_or_email} failed to login")
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")
    

# Get Market Data
@csrf_exempt
def get_market_data(request):
    data_path = 'fundsintel'
    # Get data
    data = json.loads(request.body)
    cnpjs = data.get("cnpjs")
    data_type = data.get("data_type")
    start_dt_comptc = data.get("start_dt_comptc")
    end_dt_comptc = data.get("end_dt_comptc")
    normalize = data.get("normalize")
    # Query
    cnpjs = [cnpjs] if isinstance(cnpjs, str) else cnpjs
    cnpjs_query = "'" + "', '".join(cnpjs) + "'"
    logging.info(f'Requested {data_type} from {cnpjs_query}')
    conn = sqlite3.connect(data_path + "\\" + "funds_info.db")
    query = f"""
        SELECT cnpj, dt_comptc, {data_type} as data_type
        FROM daily_info
        WHERE cnpj in ({cnpjs_query})
    """
    if start_dt_comptc:
        query += f" AND dt_comptc >= '{start_dt_comptc}'"
    if end_dt_comptc:
        query += f" AND dt_comptc <= '{end_dt_comptc}'"
    query += " ORDER BY cnpj, dt_comptc"
    market_data = pd.read_sql(query, conn)
    if normalize:
        market_data['data_type'] = market_data.groupby('cnpj')['data_type'].transform(lambda x: x / x.iloc[0] - 1)
    market_data = market_data.pivot(index='dt_comptc', columns='cnpj', values='data_type')
    market_data = market_data.to_dict()
    market_data = {cnpj: market_data[cnpj] if cnpj in market_data.keys() else "No data" for cnpj in cnpjs}
    market_information = {}
    for cnpj in market_data.keys():
        try:
            fund = InvestmentFund.objects.get(cnpj=cnpj)
            market_information[cnpj] = fund.serialize()
        except InvestmentFund.DoesNotExist:
            market_information[cnpj] = "No information"
            logging.info(f"No fund found with '{cnpj}'")
    return JsonResponse({"data": market_data, "information": market_information}, safe=False)


# Search Market Data
@csrf_exempt
def search_market_data(request):
    data = json.loads(request.body)
    query = data.get("query")
    query_results = InvestmentFund.objects.filter(Q(name__icontains=query))[:10]
    return JsonResponse({"query_results": [q.serialize() for q in query_results]}, safe=False)


# Search Single Market Data by CNPJ
@csrf_exempt
def search_single_market_data_by_cnpj(request):
    data = json.loads(request.body)
    cnpj = data.get("cnpj")
    fund = InvestmentFund.objects.filter(cnpj=cnpj)
    return JsonResponse(fund.serialize(), safe=False)




