import pandas as pd
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Apartment, Project 
from .forms import ApartmentForm, ProjectForm, UploadFileForm
from django.contrib import messages
from django.views.generic.edit import CreateView  # Correct import for CreateView
from django.views.generic.list import ListView  # Correct import for ListView
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from decimal import Decimal, InvalidOperation
from django.utils import timezone
from django.urls import reverse


class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'apartments/project_confirm_delete.html'
    context_object_name = 'project'

    def get_success_url(self):
        messages.success(self.request, "Project deleted successfully.")
        return reverse('apartments:project_list')  # Adjust 'project_list' if your URL name is different

#---------------------------------

class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'apartments/create_project.html'
    success_url = reverse_lazy('apartments:project_list')  # Redirect to a list view or another relevant page after success

#---------------------------------

class ProjectListView(ListView):
    model = Project
    template_name = 'apartments/project_list.html'
    context_object_name = 'projects'

#---------------------------------

class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'apartments/project_edit.html'  # Template for rendering the form
    success_url = reverse_lazy('apartments:project_list')  # Redirect after successful edit

#---------------------------------

from pagos.models import PriceList


def apartment_list(request, project_id=None):
    projects = Project.objects.all()
    project = None
    
    # Get apartments based on project if project_id is provided
    if project_id:
        project = get_object_or_404(Project, id=project_id)
        apartments = Apartment.objects.filter(project=project).order_by('number')
    else:
        apartments = Apartment.objects.all().order_by('number')

    # List to hold apartments with their prices and total price
    apartments_with_prices = []

    for apartment in apartments:
        selected_price_list = PriceList.objects.filter(apartment=apartment).first()
        if selected_price_list:
            apartment.current_list_price = selected_price_list.current_list_price
            total_price = apartment.area * selected_price_list.current_list_price
        else:
            apartment.current_list_price = None  # Handle case when no price is found
            total_price = None

        # Add the apartment with the price and total price
        apartments_with_prices.append({
            'apartment': apartment,
            'current_list_price': apartment.current_list_price,
            'total_price': total_price
        })

    context = {
        'apartments_with_prices': apartments_with_prices,  # Pass the list of apartments with their prices
        'projects': projects,
        'project': project,
    }

    return render(request, 'apartments/apartment_list.html', context)



#---------------------------------

def apartment_add(request):
    if request.method == 'POST':
        form = ApartmentForm(request.POST)
        if form.is_valid():
            project = form.cleaned_data['project']
            number = form.cleaned_data['number']
            
            # Check for existing apartment with the same project and number
            if Apartment.objects.filter(project=project, number=number).exists():
                messages.error(request, 'An apartment with this project and number already exists.')
            else:
                form.save()
                messages.success(request, 'Apartment added successfully!')
                return redirect('apartments:apartment_list')
    else:
        form = ApartmentForm()
    
    return render(request, 'apartments/apartment_form.html', {'form': form})

#---------------------------------

def apartment_edit(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    if request.method == 'POST':
        form = ApartmentForm(request.POST, instance=apartment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Apartment updated successfully!')  # Success message
            return redirect('apartments:apartment_list', project_id=apartment.project.pk)  # You could also redirect to a detail view
    else:
        form = ApartmentForm(instance=apartment)
    return render(request, 'apartments/apartment_form.html', {'form': form})

#---------------------------------

def apartment_delete(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    if request.method == 'POST':
        project_id = apartment.project.pk  # Get the associated project ID
        apartment.delete()
        messages.success(request, 'Apartment deleted successfully!')  # Success message
        return redirect('apartments:apartment_list', project_id=project_id)  # Redirect to the project-specific apartment list
    return render(request, 'apartments/apartment_confirm_delete.html', {'apartment': apartment})


#---------------------------------

import pandas as pd
from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import Apartment, Project  # Make sure to import your Project model
import json
import pandas as pd
from decimal import Decimal
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Apartment, Project
from .forms import UploadFileForm  # Ensure this form exists in your project

def apartment_upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Read the Excel file
            excel_file = request.FILES['file']
            try:
                # Load the Excel file into a DataFrame
                df = pd.read_excel(excel_file, header=None)  # No header in the Excel file
            except Exception as e:
                print(f"Error reading Excel file: {e}")
                return render(request, 'apartments/apartment_upload.html', {'form': form, 'error': 'Invalid Excel file format.'})

            # Iterate over the rows in the DataFrame
            for index, row in df.iterrows():
                try:
                    # Extract values from the row
                    project_name = row[0]  # First column: Project Name
                    number = row[1]        # Second column: Apartment Number
                    area = Decimal(row[2]) # Third column: Area (m2)
                    status = row[3]        # Fourth column: Status
                    points_data = row[4]   # Fifth column: Points (e.g., JSON string)

                    # Process points data
                    try:
                        points = json.loads(points_data) if isinstance(points_data, str) else points_data
                    except json.JSONDecodeError:
                        points = []  # Default to an empty list if parsing fails
                        print(f"Invalid points format in row {index}, setting to empty list.")

                    # Fetch or create the project
                    project, created = Project.objects.get_or_create(
                        name=project_name,
                        defaults={
                            'start_date': timezone.now(),  # Default start date
                        }
                    )

                    # Check if the apartment already exists
                    apartment = Apartment.objects.filter(project=project, number=number).first()

                    if apartment:
                        # Update the existing apartment
                        apartment.area = area
                        apartment.status = status if status in dict(Apartment.STATUS_CHOICES) else 'disponible'
                        apartment.points = points
                        print(f"Updating apartment: {apartment.number}")
                    else:
                        # Create a new apartment
                        apartment = Apartment(
                            project=project,
                            number=number,
                            area=area,
                            status=status if status in dict(Apartment.STATUS_CHOICES) else 'disponible',
                            points=points
                        )
                        print(f"Creating new apartment: {apartment.number}")

                    # Save the apartment (create or update)
                    apartment.save()

                except (InvalidOperation, KeyError, ValueError) as e:
                    # Handle invalid data (skip row or handle error as needed)
                    print(f"Skipping row {index} due to invalid data: {e}")
                    continue

            return redirect('apartments:project_list')
    else:
        form = UploadFileForm()

    return render(request, 'apartments/apartment_upload.html', {'form': form})


#-----------------

import pandas as pd
from decimal import Decimal
from django.shortcuts import render, redirect
from .models import Project, Apartment
from pagos.models import PriceList
from .forms import UploadFileForm  # Ensure this form exists in your project

def price_list_upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Read the Excel file
            excel_file = request.FILES['file']
            try:
                # Load the Excel file into a DataFrame
                df = pd.read_excel(excel_file, header=None)  # Adjust header if needed
            except Exception as e:
                print(f"Error reading Excel file: {e}")
                return render(request, 'price_list/price_list_upload.html', {'form': form, 'error': 'Invalid Excel file format.'})

            # Iterate over the rows in the DataFrame
            for index, row in df.iterrows():
                try:
                    # Extract values from the row
                    project_name = row[0]      # First column: Project Name
                    apartment_number = row[1] # Second column: Apartment Number
                    list_prices = row[2:8]    # Third to Eighth columns: Price List Numbers
                    current_index = int(row[8]) if not pd.isna(row[8]) else 0  # Ninth column: Current List Price Index

                    # Print values for debugging
                    print(f"Processing row {index}: Project: {project_name}, Apartment: {apartment_number}, List Prices: {list_prices}, Current Index: {current_index}")

                    # Fetch the project and apartment
                    project = Project.objects.filter(name=project_name).first()
                    if not project:
                        print(f"Skipping row {index}: Project '{project_name}' does not exist.")
                        continue

                    apartment = Apartment.objects.filter(project=project, number=apartment_number).first()
                    if not apartment:
                        print(f"Skipping row {index}: Apartment '{apartment_number}' does not exist in project '{project_name}'.")
                        continue

                    # Ensure the list prices are valid and not NaN
                    list_prices_valid = [Decimal(p) if not pd.isna(p) else None for p in list_prices]

                    # Check if list_prices_valid has valid data
                    if None in list_prices_valid:
                        print(f"Skipping row {index}: Missing data in price list values.")
                        continue

                    # Check if a price list already exists for the apartment
                    price_list = PriceList.objects.filter(apartment=apartment).first()

                    if price_list:
                        # Update the existing price list
                        price_list.list_number_0 = list_prices_valid[0]
                        price_list.list_number_1 = list_prices_valid[1]
                        price_list.list_number_2 = list_prices_valid[2]
                        price_list.list_number_3 = list_prices_valid[3]
                        price_list.list_number_4 = list_prices_valid[4]
                        price_list.list_number_5 = list_prices_valid[5]
                        price_list.current_list_price_index = current_index
                        print(f"Updating price list for apartment: {apartment.number}")
                    else:
                        # Create a new price list
                        price_list = PriceList(
                            project=project,
                            apartment=apartment,
                            list_number_0=list_prices_valid[0],
                            list_number_1=list_prices_valid[1],
                            list_number_2=list_prices_valid[2],
                            list_number_3=list_prices_valid[3],
                            list_number_4=list_prices_valid[4],
                            list_number_5=list_prices_valid[5],
                            current_list_price_index=current_index
                        )
                        print(f"Creating new price list for apartment: {apartment.number}")

                    # Save the price list (create or update)
                    price_list.save()

                except (ValueError, KeyError, Exception) as e:
                    # Handle invalid data (skip row or handle error as needed)
                    print(f"Skipping row {index} due to invalid data: {e}")
                    continue

            return redirect('apartments:project_list')
    else:
        form = UploadFileForm()

    return render(request, 'apartments/price_list_upload.html', {'form': form})

