from .forms import ProjectCostForm, ProjectTerrenoForm, ProjectFechasForm, ProjectVentasForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from dateutil.relativedelta import relativedelta
from datetime import datetime
import pandas as pd
from io import BytesIO

from .models import ProjectCost
from .desarrollo_inmobiliario_funciones import (
    calculate_apartment_payments,
    calculate_apartment_comisiones,
    calculate_hard_costs,
    calculate_soft_costs,
    calculate_project_cashflow,
    calculate_monthly_sums
)

#-------------------------------  
### 1b.0 Menú ###
#-------------------------------

def home_view(request):
    return render(request, 'analysis/analysis_home.html')

#-------------------------------

def project_cost_list(request):
    # Fetch all ProjectCost instances from the database
    project_costs = ProjectCost.objects.all()
    
    # Convert the queryset to a list of dictionaries
    project_cost_data = list(project_costs.values())
    
    
    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(project_cost_data)
    
    
    # Convert the DataFrame to HTML
    project_cost_html = df.to_html(classes='table table-striped', index=False)  # You can customize the table style
    
    # Pass the HTML table to the template
    return render(request, 'analysis/project_cost_list.html', {'project_cost_html': project_cost_html})

#-------------------------------

def delete_project_cost(request, cost_id):
    # Retrieve the specific ProjectCost instance
    project_cost = get_object_or_404(ProjectCost, id=cost_id)

    if request.method == 'POST':
        project_cost.delete()  # Delete the specific instance
        messages.success(request, 'Project cost successfully deleted!')
        return redirect('project_cost_list')  # Redirect after deletion

    # Optionally, show a confirmation page before deletion
    return render(request, 'analysis/confirm_delete.html', {'project_cost': project_cost})

#-------------------------------
### 1b.1 Edit variables ###
#-------------------------------  

def edit_project_cost(request, project_cost_id):
    # Retrieve the project cost object or return a 404 if not found
    project_cost = get_object_or_404(ProjectCost, id=project_cost_id)

    if request.method == 'POST':
        # Create a form instance with the submitted data
        form = ProjectCostForm(request.POST, instance=project_cost)
        if form.is_valid():
            # Save the updated project cost object
            form.save()
            # Redirect to the project costs list page
            return redirect('analysis:project_cost_list')
    else:
        # Create a form instance for the current project cost object
        form = ProjectCostForm(instance=project_cost)

    # Render the edit template with the form
    return render(request, 'analysis/edit_project_cost.html', {'form': form, 'project_cost': project_cost})


def edit_project_terreno(request, project_cost_id):
    # Fetch the specific cost instance
    project_cost = get_object_or_404(ProjectCost, id=project_cost_id)
    
    if request.method == 'POST':
        form = ProjectTerrenoForm(request.POST, instance=project_cost)
        if form.is_valid():
            form.save()
            return redirect('analysis:project_cost_list')  # redirect to the relevant page
    else:
        form = ProjectTerrenoForm(instance=project_cost)
    
    return render(request, 'analysis/edit_project_terreno.html', {'form': form, 'project_cost': project_cost})

def edit_project_fechas(request, project_cost_id):
    # Fetch the specific cost instance
    project_cost = get_object_or_404(ProjectCost, id=project_cost_id)
    
    if request.method == 'POST':
        form = ProjectFechasForm(request.POST, instance=project_cost)
        if form.is_valid():
            form.save()
            return redirect('analysis:project_cost_list')  # redirect to the relevant page
    else:
        form = ProjectFechasForm(instance=project_cost)
    
    return render(request, 'analysis/edit_project_fechas.html', {'form': form, 'project_cost': project_cost})

def edit_project_ventas(request, project_cost_id):
    # Fetch the specific cost instance
    project_cost = get_object_or_404(ProjectCost, id=project_cost_id)
    
    if request.method == 'POST':
        form = ProjectVentasForm(request.POST, instance=project_cost)
        if form.is_valid():
            form.save()
            return redirect('analysis:project_cost_list')  # redirect to the relevant page
    else:
        form = ProjectVentasForm(instance=project_cost)
    
    return render(request, 'analysis/edit_project_ventas.html', {'form': form, 'project_cost': project_cost})
 
#------------------------------

def project_cost_list(request):
    # Fetch all ProjectCost instances from the database
    project_costs = ProjectCost.objects.all()
    
    # Convert the queryset to a list of dictionaries
    project_cost_data = list(project_costs.values())
    
    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(project_cost_data)
    df_transposed = df.T
    
    # Convert the transposed DataFrame to HTML
    project_cost_html = df_transposed.to_html(classes='table table-striped', index=True)
    
    # Pass the HTML table to the template
    return render(request, 'analysis/project_cost_list.html', {'project_cost_html': project_cost_html, 'project_costs': project_costs})

#-------------------------------  
### 1b.3 Calculo de inteligencia ###
#-------------------------------  

@require_POST
def redirect_to_apartment_payments(request):
    project_cost_id = request.POST.get('project_cost_id')
    if project_cost_id:
        return redirect('analysis:apartment_payments', project_cost_id=project_cost_id)
    else:
        # Handle the case where project_cost_id is not provided, if necessary
        return redirect('analysis:select_project_cost')

def select_project_cost(request):
    project_costs = ProjectCost.objects.all()  # Or your logic to fetch project costs
    return render(request, 'analysis/calculate_project_analysis.html', {'project_costs': project_costs})


#-------------------------------  
def apartment_payments_view(request, project_cost_id):
    # Retrieve the project cost instance or return a 404 error if not found
    project_cost = get_object_or_404(ProjectCost, id=project_cost_id)

    # Calculate the apartment payments, which returns a pandas DataFrame
    pivot_table = calculate_apartment_payments(project_cost_id)

    # Generate HTML representation of the pivot table
    pivot_table_html = pivot_table.to_html(classes='table table-striped', index=True)

    # Render the results in a template
    return render(request, 'analysis/apartment_payments.html', {
        'project_cost': project_cost,
        'pivot_table_html': pivot_table_html,  # Pass the HTML representation
    })

#-------------------------------  

def calculate_project_ingresos(request, project_cost_id):
    # Fetch the project cost using the provided ID
    project_cost = get_object_or_404(ProjectCost, id=project_cost_id)

    # Here you can include your logic to fetch or generate the pivot_table
    # For example, you might get data from the project cost and use it to create the pivot table
    pivot_table = calculate_apartment_payments(project_cost_id)

    # Calculate monthly sums using the function provided
    monthly_sums_df = calculate_monthly_sums(pivot_table)

    # Convert the DataFrame to HTML for easy rendering in a Django template
    monthly_sums_html = monthly_sums_df.to_html(classes='table table-striped table-bordered', index=False)

    return render(request, 'analysis/calculate_ingresos.html', {
        'project_cost': project_cost,
        'monthly_sums_html': monthly_sums_html,
    })

    #-------------------------------  

def apartment_comisiones_view(request, project_cost_id):
    # Retrieve the project cost instance or return a 404 error if not found
    project_cost = get_object_or_404(ProjectCost, id=project_cost_id)

    # Calculate the apartment payments, which returns a pandas DataFrame
    pivot_table_com = calculate_apartment_comisiones(project_cost_id)
    pivot_table_html_com = pivot_table_com.to_html(classes='table table-striped', index=True)

    # Render the results in a template
    return render(request, 'analysis/apartment_comisiones.html', {
        'project_cost': project_cost,
        'pivot_table_html': pivot_table_html_com,  # Pass the HTML representation
    })

#-------------------------------  

def calculate_hard_costs_view(request, project_cost_id):
    project_cost = get_object_or_404(ProjectCost, id=project_cost_id)
    
    # Calculating the hard costs
    total_hard_cost = calculate_hard_costs(project_cost_id)
    
    return render(request, 'analysis/calculate_hard_costs.html', {
        'project_cost': project_cost,
        'total_hard_cost': total_hard_cost,
    })

#------------------------------- 

def calculate_soft_costs_view(request, project_cost_id):
    project_cost = get_object_or_404(ProjectCost, id=project_cost_id)
    
    # Calculating the hard costs
    total_soft_cost = calculate_soft_costs(project_cost_id)
    total_soft_cost = total_soft_cost.applymap(lambda x: f"${x:,.0f}" if isinstance(x, (int, float)) else x)
    total_soft_cost_html = total_soft_cost.to_html(classes='table table-striped')
    
    return render(request, 'analysis/calculate_softcost.html', {
        'project_cost': project_cost,
        'total_soft_cost': total_soft_cost_html,
    })

#-------------------------------  

def calculate_project_cashflow_view(request, project_cost_id):
    project_cost = get_object_or_404(ProjectCost, id=project_cost_id)
    
    # Calculating the hard costs
    total_cash_flow = calculate_project_cashflow(project_cost_id)
    total_cash_flow = total_cash_flow.applymap(lambda x: f"${x:,.0f}" if isinstance(x, (int, float)) else x)
    total_cash_flow_html = total_cash_flow.to_html(classes='table table-striped')
    
    return render(request, 'analysis/calculate_cashflow.html', {
        'project_cost': project_cost,
        'total_cash_flow': total_cash_flow_html,
    })

#-------------------------------  

def redirect_to_view(request):
    if request.method == "POST":
        project_cost_id = request.POST.get("project_cost_id")
        action = request.POST.get("action")
        
        if action == "apartment_payments":
            # Redirect to the apartment payments view
            return redirect('analysis:apartment_payments', project_cost_id=project_cost_id)
        elif action == "apartment_comisiones":
            # Redirect to the soft costs calculation view
            return redirect('analysis:apartment_comisiones', project_cost_id=project_cost_id)
        elif action == "soft_costs":
            # Redirect to the soft costs calculation view
            return redirect('analysis:calculate_soft_costs', project_cost_id=project_cost_id)
        elif action == "calculate_flujo":
            # Redirect to the soft costs calculation view
            return redirect('analysis:calculate_flujo', project_cost_id=project_cost_id)
    
    # In case of an invalid request, you can redirect back to the form or handle the error as needed
    return redirect('analysis:select_project_cost')


#---------------------------------
### Excel Export Section ###
#---------------------------------

def download_excel_view_ingresos(request, project_cost_id):
    # Retrieve project cost instance or return a 404 error if not found
    project_cost = get_object_or_404(ProjectCost, id=project_cost_id)

    # Calculate apartment payments and return a DataFrame
    pivot_table = calculate_apartment_payments(project_cost_id)

    # Create an Excel file in memory
    excel_file = BytesIO()
    pivot_table.to_excel(excel_file, index=True, engine='openpyxl')
    excel_file.seek(0)

    # Create HTTP response for downloading the Excel file
    response = HttpResponse(
        excel_file.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename=apartment_payments_{project_cost_id}.xlsx'

    return response


def download_excel_view_comisiones(request, project_cost_id):
    # Retrieve project cost instance or return a 404 error if not found
    project_cost = get_object_or_404(ProjectCost, id=project_cost_id)

    # Calculate apartment commissions and return a DataFrame
    pivot_table = calculate_apartment_comisiones(project_cost_id)

    # Create an Excel file in memory
    excel_file = BytesIO()
    pivot_table.to_excel(excel_file, index=True, engine='openpyxl')
    excel_file.seek(0)

    # Create HTTP response for downloading the Excel file
    response = HttpResponse(
        excel_file.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename=apartment_comisiones_{project_cost_id}.xlsx'

    return response


def download_excel_view_softcost(request, project_cost_id):
    # Calculate soft costs and return a DataFrame
    pivot_table = calculate_soft_costs(project_cost_id)

    # Create an Excel file in memory
    excel_file = BytesIO()
    pivot_table.to_excel(excel_file, index=True, engine='openpyxl')
    excel_file.seek(0)

    # Create HTTP response for downloading the Excel file
    response = HttpResponse(
        excel_file.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename=softcost_{project_cost_id}.xlsx'

    return response


def download_excel_view_flujo(request, project_cost_id):
    # Retrieve project cost instance or return a 404 error if not found
    project_cost = get_object_or_404(ProjectCost, id=project_cost_id)

    # Calculate project cash flow and return a DataFrame
    pivot_table = calculate_project_cashflow(project_cost_id)

    # Create an Excel file in memory
    excel_file = BytesIO()
    pivot_table.to_excel(excel_file, index=True, engine='openpyxl')
    excel_file.seek(0)

    # Create HTTP response for downloading the Excel file
    response = HttpResponse(
        excel_file.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename=flujo_{project_cost_id}.xlsx'

    return response
