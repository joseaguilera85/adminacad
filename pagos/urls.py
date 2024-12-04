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
    path('apartamento/<int:apartment_number>/', views.apartment_detail, name='apartment_detail'),

    #### 3.2b Vista edificio ####
    path('canva/', views.plano, name='plano'),
    path('canva/add/', views.add_house, name='add_house'),
    path("canva/edit/<int:pk>/", views.edit_house, name="edit_house"),
    path('canva/delete/<int:pk>/', views.delete_house, name='delete_house'),  # Add the delete URL
    path('canva/upload/', views.upload_excel, name='upload_excel'),
    path('canva/delete_all_houses/', views.delete_all_houses, name='delete_all_houses'),
    

    #### 3.3 Cotización ###
    path('cotizacion/', views.cotizacion, name='cotizacion'), # COTIZACION
    path('plan-pagos/', views.payment_plan_view, name='plan_pagos'),  # Ruta para 'plan-pagos/'
    
    #### 3.4 Proceso de venta o apartado ###
    path('venta/', views.apartado_venta, name='lista_departamentos'),
    path('venta/<int:apartment_id>/', views.ventas, name='venta'),
    path('apartar/<int:apartment_id>/', views.apartar, name='apartar'),
    path('disponible/<int:apartment_id>/', views.disponible_view, name='disponible'),

    #### 3.6 Pagos y estado de cuenta $$$
    path('payment_records/', views.list_payment_records, name='list_payment_records'),
    path('record/<int:pk>/', views.record_detail_view, name='record_detail'), #Detalle de pan de pagos
    path('delete/<int:id>/', views.delete_record, name='delete_record'),
    path('register/<int:payment_record_id>/', views.register_payment, name='register_payment'),
    
    path('toggle-payment/<int:installment_id>/', views.toggle_payment_status, name='toggle_payment'),
    path('cancel-payment/<int:installment_id>/', views.cancel_payment, name='cancel_payment'),

    
    #### Otros ###
    path('clientes/', views.cliente_list_view, name='lista_clientes'),

    
]

