from django.urls import path
from .views import (
    home_view, project_cost_list, delete_project_cost, 
    edit_project_cost, edit_project_terreno, edit_project_fechas, edit_project_ventas,
    apartment_payments_view, 
    redirect_to_apartment_payments, select_project_cost,
    calculate_project_ingresos, apartment_comisiones_view,
    calculate_hard_costs_view, download_excel_view_ingresos,
    apartment_payments_view, download_excel_view_comisiones,
    redirect_to_view, download_excel_view_softcost,
    calculate_soft_costs_view, calculate_project_cashflow_view,
    download_excel_view_flujo
)

app_name = 'analysis'

# URL patterns for the application
urlpatterns = [
    # Home page
    path('', home_view, name='analysis_home'),

    # Project Analysis and Selections
    path('project-analysis/', select_project_cost, name='select_project_cost'),  # Select project cost for analysis
    path('redirect-to-apartment-payments/', redirect_to_apartment_payments, name='redirect_to_apartment_payments'),  # Redirect to apartment payments

    # Project COST
    path('project-cost/list/', project_cost_list, name='project_cost_list'),  # List view
    
    path('project-cost/<int:project_cost_id>/edit_cost/', edit_project_cost, name='edit_project_cost'),  # Edit project cost
    path('project-cost/<int:project_cost_id>/edit_terreno/', edit_project_terreno, name='edit_project_terreno'),  # Edit project cost
    path('project-cost/<int:project_cost_id>/edit_fechas/', edit_project_fechas, name='edit_project_fechas'),  # Edit project cost
    path('project-cost/<int:project_cost_id>/edit_ventas/', edit_project_ventas, name='edit_project_ventas'),  # Edit project cost
    
    path('project-cost/delete/<int:cost_id>/', delete_project_cost, name='delete_project_cost'),  # Delete project cost


    # Apartment Payments and Ingresos
    path('apartment-payments/<int:project_cost_id>/', apartment_payments_view, name='apartment_payments'),  # View apartment payments
    path('apartment-payments/<int:project_cost_id>/download/', download_excel_view_ingresos, name='download_excel_ing'),  # Download apartment payments

    # Apartment Commissions
    path('apartment-comisiones/<int:project_cost_id>/', apartment_comisiones_view, name='apartment_comisiones'),  # View apartment commissions
    path('apartment-comisiones/<int:project_cost_id>/download/', download_excel_view_comisiones, name='download_excel_com'),  # Download commissions

    # Project Hard Costs
    path('calculate-hard-costs/<int:project_cost_id>/', calculate_hard_costs_view, name='calculate_hard_costs'),  # Calculate hard costs

    # Project Soft Costs
    path('calculate-soft-costs/<int:project_cost_id>/', calculate_soft_costs_view, name='calculate_soft_costs'),  # Calculate soft costs
    path('calculate-soft-costs/<int:project_cost_id>/download/', download_excel_view_softcost, name='download_excel_sof'),  # Download soft costs

    # Project Cash Flow
    path('calculate-cashflow/<int:project_cost_id>/', calculate_project_cashflow_view, name='calculate_flujo'),  # Calculate cash flow
    path('calculate-cashflow/<int:project_cost_id>/download/', download_excel_view_flujo, name='download_excel_flu'),  # Download cash flow

    # Generic Redirect
    path('redirect-to-view/', redirect_to_view, name='redirect_to_view'),  # Redirect to specified view
]
