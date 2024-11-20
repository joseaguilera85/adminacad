from django.urls import path
from . import views

app_name = 'pagos'  # Set the app name for namespacing

urlpatterns = [
    path('home/', views.menu, name='payments_index'),  # Página de índice para 'payments/'
    
    #### 3.1 Lista de precios ###
    path('price-list/', views.price_list_view, name='price_list'),
    path('price-list/edit/<int:apartment_id>/values/', views.edit_price_list_values, name='edit_price_list_values'),
    path('price-list/edit/<int:apartment_id>/current-index/', views.edit_current_price_list_index, name='edit_current_price_list_index'),

    #### 3.2a Inventario ####
    path('inventario/', views.inventario_view, name='inventario'),
    
    #### 3.2b Vista edificio ####
    path('plan-edificio/', views.plan_edificio_view, name='plan_edificio'),
    path('plan-edificio/apartamento/<int:apartment_number>/', views.apartment_detail, name='apartment_detail'),

    #### 3.3 Cotización ###
    path('cotizacion/', views.select_apartment_view, name='cotizacion'), # COTIZACION
    path('plan-pagos/', views.payment_plan_view, name='plan_pagos'),  # Ruta para 'plan-pagos/'
    
    #### 3.4 Proceso de venta o apartado ###
    path('venta/', views.review_apartments_view, name='lista_departamentos'),
    path('venta/<int:apartment_id>/', views.ventas, name='venta'),
    path('apartar/<int:apartment_id>/', views.apartar, name='apartar'),
    path('disponible/<int:apartment_id>/', views.disponible_view, name='disponible'),

    #### 3.6 Pagos y estado de cuenta $$$
    path('payment_records/', views.list_payment_records, name='list_payment_records'),
    path('record/<int:pk>/', views.record_detail_view, name='record_detail'), #Detalle de pan de pagos
    path('delete/<int:id>/', views.delete_record, name='delete_record'),
    path('register/<int:payment_record_id>/', views.register_payment, name='register_payment'),
    path('account-statement/<int:payment_record_id>/', views.account_statement, name='account_statement'),
    
    #### Otros ###
    path('clientes/', views.cliente_list_view, name='lista_clientes'),
    path('calculate-npv/<int:payment_record_id>/', views.CalculateNPVView.as_view(), name='calculate_npv')

    
]

