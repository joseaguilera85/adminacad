from datetime import datetime, timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.timezone import make_aware

from .forms import (
    ClienteForm,
    EventForm,
    InteractionForm,
    MeetingForm,
    OportunidadForm,
    CreateOportunidadForm,
    SignUpForm,
)
from .models import Cliente, Event, Interaction, Meeting, Oportunidad
from apartments.models import Apartment, Project


### 2.0 Login ###
# Logout the user and redirect to the login page
def logout_view(request):
    logout(request)
    return redirect('menu:login')

#------------------------------------------

# Home page view for authenticated users
@login_required
def client_home(request):
    return render(request, 'clientes/clientes_home.html')

#------------------------------------------
def custom_403(request, exception=None): 
    return render(request, 'clientes/403.html', status=403)
#------------------------------------------

#------------------------
### 2.1 Clientes ###
#------------------------

# Create a new client
@login_required
def new_client(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)  # Don't save to the database yet
            cliente.created_by = request.user  # Set the created_by field to the currently logged-in user
            cliente.save()  # Now save the instance to the database
            return redirect('clientes:consult_clients')
    else:
        form = ClienteForm()
        # If the form is not valid, print the error messages
        print("Form is not valid")
    return render(request, 'clientes/add_client.html', {'form': form})

#---------------------------------------------
# Consult and filter clients based on search criteria

@login_required
def consult_clients(request):

    search_query = request.GET.get('search', '')
    clients = Cliente.objects.filter(
        Q(nombre__icontains=search_query) |
        Q(apellido__icontains=search_query) |
        Q(mail__icontains=search_query) |
        Q(celular__icontains=search_query)
    ) if search_query else Cliente.objects.all()

    # Paginate the clients
    paginator = Paginator(clients, 10)  # 10 clients per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'clientes/client_list.html', {'page_obj': page_obj})

#---------------------------------------------

# Delete a client by ID
@login_required
def delete_client(request, client_id):
    cliente = get_object_or_404(Cliente, id_cliente=client_id)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Client deleted successfully!')
        return redirect('clientes:consult_clients')
    return render(request, 'clientes/client_list.html', {'cliente': cliente})

#---------------------------------------------

# Display detailed information about a client, including their interactions
@login_required
def client_detail(request, id_cliente):
    client = get_object_or_404(Cliente, id_cliente=id_cliente)
    oportunidades = client.oportunidades.all()
    interactions = client.interactions.all()
    return render(request, 'clientes/client_detail.html', {'client': client, 'oportunidades': oportunidades})

#---------------------------------------------

# Edit an existing client's details
@login_required
def edit_client(request, id_cliente):
    client = get_object_or_404(Cliente, id_cliente=id_cliente)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client details updated successfully!')
            return redirect('clientes:client_detail', id_cliente=id_cliente)
    else:
        form = ClienteForm(instance=client)
    return render(request, 'clientes/edit_client.html', {'form': form, 'client': client})

#------------------------
### 2.2 Oportunidades ###
#------------------------

@login_required
def review_oportunidades(request):

    oportunidades = Oportunidad.objects.all()
    return render(request, 'clientes/oportunidades_list.html', {'oportunidades': oportunidades})

#-----------------

@login_required
def create_oportunidad(request, id_cliente):
    client = get_object_or_404(Cliente, id_cliente=id_cliente)
    
    if request.method == 'POST':
        form = CreateOportunidadForm(request.POST)
        
        if form.is_valid():
            oportunidad = form.save(commit=False)
            oportunidad.cliente = client
            oportunidad.estatus = 'prospecto'
            oportunidad.created_by = request.user
            oportunidad.created_at = timezone.now()
            oportunidad.save()
            messages.success(request, 'Oportunidad creada exitosamente!')
            return redirect('clientes:client_detail', id_cliente=id_cliente)
    else:
        form = CreateOportunidadForm()

    return render(request, 'clientes/create_oportunidad.html', {'form': form, 'client': client})


#-----------------

def edit_oportunidad(request, id_oportunidad):
    oportunidad = get_object_or_404(Oportunidad, id_oportunidad=id_oportunidad)
    cliente = oportunidad.cliente  # Access related Cliente
    project = oportunidad.project  # Access related Project
    
    if request.method == 'POST':
        form = OportunidadForm(request.POST, instance=oportunidad)
        if form.is_valid():
            form.save()
            messages.success(request, "Interaction updated successfully!")
            return redirect('clientes:review_oportunidades')  # Redirect to the list view
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = OportunidadForm(instance=oportunidad)

        return render(request, 'clientes/edit_oportunidad.html', {
        'form': form,
        'oportunidad': oportunidad,
        'cliente': cliente,
        'project': project,
    })



#------------------------
### 2.2 Interacciones ###
#------------------------


@login_required
def review_interacciones(request, id_oportunidad):
    oportunidad = get_object_or_404(Oportunidad, id_oportunidad=id_oportunidad)
    interactions = oportunidad.interactions.all()
    return render(request, 'clientes/interacciones_list.html', {'oportunidad': oportunidad, 'interactions': interactions})

#---------------------------------------------

# Add an interaction for a specific client
@login_required
def add_interaction(request, id_cliente):
    client = get_object_or_404(Cliente, id_cliente=id_cliente)
    if request.method == 'POST':
        form = InteractionForm(request.POST)
        if form.is_valid():
            interaction = form.save(commit=False)
            interaction.cliente = client
            interaction.save()
            messages.success(request, 'Interaction added successfully!')
            return redirect('clientes:client_detail', id_cliente=id_cliente)
    else:
        form = InteractionForm(initial={'cliente': client})
        form.fields['oportunidad'].queryset = client.oportunidades.all()

        
    return render(request, 'clientes/add_interaction.html', {'form': form, 'client': client})


#---------------------------------------------
### 2.3 Citas ###
#---------------------------------------------

@login_required
def schedule_meeting(request):
    cliente_id = request.GET.get('client')

    if request.method == 'POST':
        form = MeetingForm(request.POST, cliente_id=cliente_id)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting_date_time = make_aware(meeting.date_time)

            # Check for conflicting meetings
            conflicting_meetings = Meeting.objects.filter(
                salesperson=meeting.salesperson,
                date_time__range=(meeting_date_time - timedelta(minutes=30), meeting_date_time + timedelta(minutes=30))
            )
            if conflicting_meetings.exists():
                messages.error(request, 'This salesperson is already booked at the selected time. Please choose another time.')
                last_message = list(messages.get_messages(request))[-1:]
                return render(request, 'clientes/add_meeting.html', {'form': form, 'last_message': last_message})
            
            # Save the meeting
            meeting.save()
            
            # Find the related Oportunidad
            oportunidad = Oportunidad.objects.filter(cliente=meeting.client).first()
            if not oportunidad:
                messages.error(request, 'No opportunity found for this client.')
                last_message = list(messages.get_messages(request))[-1:]
                return render(request, 'clientes/add_meeting.html', {'form': form, 'last_message': last_message})

            # Automatically create an interaction for the meeting
            try:
                Interaction.objects.create(
                    cliente=meeting.client,
                    oportunidad=oportunidad,
                    salesperson=meeting.salesperson,
                    interaction_type='Meeting',
                    category='Follow-up',
                    notes=f"Scheduled a meeting on {meeting.date_time.strftime('%Y-%m-%d %H:%M')}"
                )
            except Exception as e:
                messages.error(request, f"An error occurred while creating the interaction: {str(e)}")
                last_message = list(messages.get_messages(request))[-1:]
                return render(request, 'clientes/add_meeting.html', {'form': form, 'last_message': last_message})

            messages.success(request, 'Meeting scheduled successfully!')
            return redirect('clientes:clientes_home')
        else:
            # Debug form errors for troubleshooting
            print(form.errors)

    else:
        # Initialize the form for GET requests
        form = MeetingForm(cliente_id=cliente_id)

    return render(request, 'clientes/add_meeting.html', {'form': form})

#---------------------------------------------

@login_required
def meeting_list(request):
    # Check for permission
    if not request.user.has_perm('clientes.view_meeting'):
        return render(request, 'clientes/403.html', status=403)
    
    start_date = request.GET.get('start_date', None)
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date() if start_date else timezone.now().date() - timedelta(days=timezone.now().weekday())
    end_of_week = start_date + timedelta(days=6)
    meetings = Meeting.objects.filter(date_time__range=[start_date, end_of_week]).order_by('date_time')
    days = [start_date + timedelta(days=i) for i in range(7)]
    return render(request, 'clientes/meeting_list.html', {'meetings': meetings, 'current_week_start': start_date, 'current_week_end': end_of_week, 'days': days})

#---------------------------------------------


# Edit an existing meeting
@login_required
def edit_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            form.save()
            messages.success(request, 'Meeting updated successfully!')
            return redirect('clientes:meeting_list')
    else:
        form = MeetingForm(instance=meeting)
    return render(request, 'clientes/edit_meeting.html', {'form': form, 'meeting': meeting})

#---------------------------------------------

# Delete a meeting by ID
@login_required
def delete_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    if request.method == 'POST':
        meeting.delete()
        messages.success(request, 'Meeting deleted successfully!')
        return redirect('clientes:meeting_list')
    return render(request, 'clientes/delete_meeting.html', {'meeting': meeting})



#---------------------------------------------
### 2.4 Dashboard ###
#---------------------------------------------

def dashboard_view(request):
    return render(request, 'clientes/dashboard.html')

#---------------------------------------------

def oportunidad_list(request):
    # Get all opportunities
    oportunidades = Oportunidad.objects.all()

    # Render the template with the 'oportunidades' context
    return render(request, 'clientes/oportunidades_list.html', {'oportunidades': oportunidades})


#---------------------------------------------

from django.shortcuts import render
from django.db.models import Count, Q
from .models import Cliente

def tabular_leads(request):
    # Fetch data from the Oportunidad model
    project_data = Oportunidad.objects.values('project__name') \
        .annotate(total_leads=Count('id_oportunidad', filter=Q(estatus='prospecto'))) \
        .annotate(total_clients=Count('id_oportunidad', filter=Q(estatus='cerrado'))) \
        .annotate(conversion_rate=100.0 * Count('id_oportunidad', filter=Q(estatus='cerrado')) / Count('id_oportunidad', filter=Q(estatus='prospecto'))) \
        .order_by('project__name')

    # Pass data to the template
    context = {
        'project_data': project_data,
    }
    return render(request, 'clientes/tabular_dashboard.html', context)


#---------------------------------------------

def apartment_status_report(request):
    # Get the selected project and status from the GET parameters
    selected_project_id = request.GET.get('project')
    status = request.GET.get('status')

    # Get all projects for the dropdown
    projects = Project.objects.all()

    # Query apartments if a project is selected, and filter by status if a status is selected
    apartments = Apartment.objects.all()

    # Apply project filter if a project is selected
    if selected_project_id:
        apartments = apartments.filter(project_id=selected_project_id)
    
    # Apply status filter if a status is selected
    if status:
        apartments = apartments.filter(status=status)

    # Pass the filtered apartments and projects to the template
    context = {
        'apartments': apartments,
        'projects': projects,
        'selected_project_id': selected_project_id,
        'status': status,
    }

    return render(request, 'clientes/status_report.html', context)



#---------------------------------------------
### 2.5 Eventos ###
#---------------------------------------------

def event_list(request):
    # Fetch events created by the logged-in user
    events = Event.objects.filter(creator=request.user).order_by('-date')

    return render(request, 'clientes/event_list.html', {'events': events})


#---------------------------------------------

@login_required
def create_event(request):
    # Ensure the user belongs to the 'ventas' group
    if not request.user.groups.filter(name='Ventas').exists():
        return render(request, 'clientes/403.html', {"message": "You do not have permission to create events."})
    
    if request.method == 'POST':
        form = EventForm(request.POST)
        # Set the correct queryset for the invited_clients field before validating
        form.fields['invited_clients'].queryset = Cliente.objects.all()  # No filtering applied
        
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.save()
            invited_clients = form.cleaned_data['invited_clients']
            event.invited_clients.set(form.cleaned_data['invited_clients'])

                        # Send email to each invited client
            for client in invited_clients:
                send_mail(
                    subject=f"You are invited to {event.title}",  # Replace `event.name` with the event name field
                    message=f"Dear {client.nombre},\n\nYou are invited to the event '{event.title}'. Please join us on {event.date}.",
                    from_email=settings.DEFAULT_FROM_EMAIL,  # Make sure this is configured in your settings
                    recipient_list=[client.mail],
                    fail_silently=False,
                )

            return redirect('clientes:event_list')
    else:
        form = EventForm()
        # Allow all clients to be listed for selection
        form.fields['invited_clients'].queryset = Cliente.objects.all()

    return render(request, 'clientes/create_event.html', {'form': form})


#---------------------------------------------

def edit_event(request, id_event):
    event = get_object_or_404(Event, id_event=id_event)
    
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        form.fields['invited_clients'].queryset = Cliente.objects.all()  # Ensure queryset is set for POST
        if form.is_valid():
            form.save()
            return redirect('clientes:event_list')  # Redirect after saving
    else:
        form = EventForm(instance=event)
        form.fields['invited_clients'].queryset = Cliente.objects.all()  # Ensure queryset is set for GET
    
    return render(request, 'clientes/edit_event.html', {'form': form, 'event': event})




#---------------------------------------------

def delete_event(request, id_event):
    event = get_object_or_404(Event, id_event=id_event)
    
    if request.method == 'POST':
        event.delete()
        return redirect('clientes:event_list')  # Adjust to redirect to your event list or another relevant page
    
    return render(request, 'clientes/delete_event.html', {'event': event})