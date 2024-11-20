# bancos/urls.py
from django.urls import path
from . import views

app_name = "bancos"

urlpatterns = [
    path('deposit/<str:account_number>/', views.deposit, name='deposit'),
    path('withdraw/<str:account_number>/', views.withdraw, name='withdraw'),
    path('transactions/<str:account_number>/', views.account_transactions, name='account_transactions'),
    path('cuentas/', views.bank_account_list, name='bank_account_list'),
    path('menu/', views.bancos_menu, name='bancos_menu'),
]
