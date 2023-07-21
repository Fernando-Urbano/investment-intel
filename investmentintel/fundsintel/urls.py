
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("get-market-data", views.get_market_data, name="get_market_data"),
    path("search-market-data", views.search_market_data, name="search_market_data"),
]
