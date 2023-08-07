from django.urls import path 
from . import views


urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("deposit/", views.DepositView.as_view(), name="deposit"),
    path("withdraw/", views.WithdrawView.as_view(), name="withdraw"),
    path("transfer/", views.TransferView.as_view(), name="transfer"),
    path("api/suggest/", views.API.suggest, name="suggest")
]
