# egresos/urls.py
from django.urls import path
from . import views


app_name = 'egresos'

urlpatterns = [
    path('', views.main_menu, name='egresos_menu'),
    path('menu/', views.main_menu, name='egresos_menu'),
    
    path('egresos/', views.lista_egresos, name='lista_egresos'),  # URL for listing expenses
    
    
    path('ventor/add/', views.add_vendor, name='add_vendor'),
    path('vendor/list/', views.vendor_list, name='vendor_list'),  # URL for the vendor list page
    path('vendor/edit/<int:pk>/', views.edit_vendor, name='edit_vendor'),  # Edit vendor
    path('vendor/delete/<int:pk>/', views.delete_vendor, name='delete_vendor'),  # Delete vendor

    path('purchase_order_list/', views.purchase_order_list, name='purchase_order_list'),
    path('view_purchase_order/<int:purchase_order_id>/', views.view_purchase_order_item, name='view_purchase_order'),
    
    path('create_purchase_order/', views.create_purchase_order, name='create_purchase_order'),
    path('create_purchase_order_item/<int:purchase_order_id>/', views.create_purchase_order_item, name='create_purchase_order_item'),
    path('purchase-orders/<int:order_id>/edit/', views.edit_purchase_order, name='edit_purchase_order'),
    path('purchase-orders/<int:order_id>/delete/', views.delete_purchase_order, name='delete_purchase_order'),

    path('purchase-orders/<int:purchase_order_id>/items/<int:item_id>/edit/', views.edit_purchase_order_item, name='edit_purchase_order_item'),
    path('purchase-orders/<int:purchase_order_id>/items/<int:item_id>/delete/', views.delete_purchase_order_item, name='delete_purchase_order_item'),

    path('almacen/', views.almacen, name='almacen'),

]
