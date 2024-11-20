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
            return redirect('apartment_list', project_id=apartment.project.pk)  # You could also redirect to a detail view
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

def apartment_upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Read the CSV file
            csv_file = request.FILES['file']
            df = pd.read_csv(csv_file, header=None)  # No header in your CSV example

            for index, row in df.iterrows():
                try:
                    # Extract values from the row
                    project_name = row[0]  # First column: Project Name
                    number = row[1]        # Second column: Apartment Number
                    area = Decimal(row[2]) # Third column: Area (m2)
                    price_per_m2 = Decimal(row[3]) # Fourth column: Price per m2
                    status = row[4]        # Fifth column: Status

                    # Fetch the project by name or create it if it doesn't exist
                    project, created = Project.objects.get_or_create(
                        name=project_name,
                        defaults={
                            'start_date': timezone.now(),  # Set a default start date
                            # Add other required fields here with default values if needed
                        }
                    )

                    # Create the Apartment object
                    apartment = Apartment(
                        project=project,  # Associate the apartment with the project
                        number=number,
                        area=area,
                        price_per_m2=price_per_m2,
                        status=status if status in dict(Apartment.STATUS_CHOICES) else 'disponible'  # Validate status
                    )
                    print("Saving apartment:", apartment.number)
                    apartment.save()

                except (InvalidOperation, KeyError, ValueError) as e:
                    # Handle invalid data (skip row or handle error as needed)
                    print(f"Skipping row {index} due to invalid data: {e}")
                    continue  # Skip the current iteration if there's an error

            return redirect('apartments:project_list')
    else:
        form = UploadFileForm()

    return render(request, 'apartments/apartment_upload.html', {'form': form})
