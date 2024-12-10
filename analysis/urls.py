from django.urls import path
from . import views

app_name = 'analysis'

# URL patterns for the application
urlpatterns = [
    # Home page
    path('', views.home_view, name='analysis_home'),
    path('projects/', views.project_list, name='project_list'),
    path('project/<int:project_cost_id>/', views.project_detail, name='project_detail'),


    # Project Analysis and Selections
    path('project-analysis/', views.select_project_cost, name='select_project_cost'),  # Select project cost for analysis
    path('redirect-to-apartment-payments/', views.redirect_to_apartment_payments, name='redirect_to_apartment_payments'),  # Redirect to apartment payments

    # Project COST
    path('project-cost/list/', views.project_cost_list, name='project_cost_list'),  # List view
    
    path('project-cost/<int:project_cost_id>/edit_cost/', views.edit_project_cost, name='edit_project_cost'),  # Edit project cost
    path('project-cost/<int:project_cost_id>/edit_terreno/', views.edit_project_terreno, name='edit_project_terreno'),  # Edit project cost
    path('project-cost/<int:project_cost_id>/edit_fechas/', views.edit_project_fechas, name='edit_project_fechas'),  # Edit project cost
    path('project-cost/<int:project_cost_id>/edit_ventas/', views.edit_project_ventas, name='edit_project_ventas'),  # Edit project cost
    
    path('project-cost/delete/<int:cost_id>/', views.delete_project_cost, name='delete_project_cost'),  # Delete project cost


    # Apartment Payments and Ingresos
    path('apartment-payments/<int:project_cost_id>/', views.apartment_payments_view, name='apartment_payments'),  # View apartment payments
    path('apartment-payments/<int:project_cost_id>/download/', views.download_excel_view_ingresos, name='download_excel_ing'),  # Download apartment payments

    # Apartment Commissions
    path('apartment-comisiones/<int:project_cost_id>/', views.apartment_comisiones_view, name='apartment_comisiones'),  # View apartment commissions
    path('apartment-comisiones/<int:project_cost_id>/download/', views.download_excel_view_comisiones, name='download_excel_com'),  # Download commissions

    # Project Hard Costs
    path('calculate-hard-costs/<int:project_cost_id>/', views.calculate_hard_costs_view, name='calculate_hard_costs'),  # Calculate hard costs

    # Project Soft Costs
    path('calculate-soft-costs/<int:project_cost_id>/', views.calculate_soft_costs_view, name='calculate_soft_costs'),  # Calculate soft costs
    path('calculate-soft-costs/<int:project_cost_id>/download/', views.download_excel_view_softcost, name='download_excel_sof'),  # Download soft costs

    # Project Cash Flow
    path('calculate-cashflow/<int:project_cost_id>/', views.calculate_project_cashflow_view, name='calculate_flujo'),  # Calculate cash flow
    path('calculate-cashflow/<int:project_cost_id>/download/', views.download_excel_view_flujo, name='download_excel_flu'),  # Download cash flow

    # Generic Redirect
    path('redirect-to-view/', views.redirect_to_view, name='redirect_to_view'),  # Redirect to specified view
]
