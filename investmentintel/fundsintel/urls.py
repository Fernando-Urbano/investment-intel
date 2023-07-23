
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("get-market-data", views.get_market_data, name="get_market_data"),
    path("search-market-data", views.search_market_data, name="search_market_data"),
    path("search-single-market-data-by-cnpj", views.search_single_market_data_by_cnpj, name="search_single_market_data_by_cnpj"),
]
