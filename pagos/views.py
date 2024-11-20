from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import PaymentPlanForm, PriceListForm
from .models import (
    Apartment,
    PaymentRecord,
    ListaCliente,
    PriceList,
    Project,
    PaymentTransaction,
    AccountStatement,
)
from apartments.models import Apartment
from clientes.models import Cliente
from datetime import datetime, timedelta
from decimal import Decimal
import calendar
from django.utils import timezone

# -------------------------------

def menu(request):
    return render(request, 'pagos/index.html')

# -------------------------------
#### 3.1 Lista de precios ###
# -------------------------------

def price_list_view(request):
    # Get all projects for the dropdown
    projects = Project.objects.all()
    
    # Get the selected project ID from the GET request
    selected_project_id = request.GET.get('project')
    
    # Filter apartments based on the selected project, or get all apartments if no project is selected
    if selected_project_id:
        apartments = Apartment.objects.filter(project_id=selected_project_id)
    else:
        apartments = Apartment.objects.all()

    # Get price lists if needed, you can modify this as per your requirement
    price_lists = PriceList.objects.filter(apartment__in=apartments)

    context = {
        'projects': projects,
        'selected_project_id': selected_project_id,
        'apartments': apartments,
        'price_lists': price_lists,
    }
    return render(request, 'pagos/price_list.html', context)

#------------------------------

def edit_price_list_values(request, apartment_id):
    price_list, created = PriceList.objects.get_or_create(apartment_id=apartment_id)

    if request.method == 'POST':
        form = PriceListForm(request.POST, instance=price_list)
        if form.is_valid():
            form.save()
            return redirect('pagos:price_list')  # Redirect to the price list view
    else:
        form = PriceListForm(instance=price_list)

    context = {
        'form': form,
        'price_list': price_list,
    }
    return render(request, 'pagos/edit_price_list_values.html', context)

#------------------------------

def edit_current_price_list_index(request, apartment_id):
    price_list = get_object_or_404(PriceList, apartment_id=apartment_id)

    if request.method == 'POST':
        price_list.current_list_price_index = request.POST.get('current_list_price_index')
        price_list.save()
        return redirect('pagos:price_list')  # Redirect to the price list view

    context = {
        'price_list': price_list,
    }
    return render(request, 'pagos/edit_current_price_list_index.html', context)


#------------------------------
#### 3.2a Inventario ####
#------------------------------


def inventario_view(request):
    project_name_filter = request.GET.get('project_name', '')  # Get filter value from query parameters
    
    # Get all projects to populate the dropdown
    all_projects = Project.objects.all()
    
    if project_name_filter:
        projects = Project.objects.prefetch_related('apartments').filter(name=project_name_filter)
    else:
        projects = Project.objects.prefetch_related('apartments').all()

    return render(request, 'pagos/inventario.html', {
        'projects': projects,
        'all_projects': all_projects,  # Pass all project names for the dropdown
        'project_name_filter': project_name_filter,  # Pass the current filter to the template
    })


#------------------------------
#### 3.2b Vista edificio ####
# -----------------------------

def plan_edificio_view(request):
    building = []
    for piso in range(1, 9):  # Floors from 1 to 8
        floor = {
            'number': piso,
            'apartments': [((piso - 1) * 3 + depto) for depto in range(1, 4)]
        }
        building.append(floor)
    building.reverse()  # Reverse the order of floors so that Floor 1 is at the bottom
    return render(request, 'pagos/plan_edificio.html', {'building': building})



#------------------------------

def apartment_detail(request, apartment_number):
    # Retrieve the apartment by its number
    apartment = get_object_or_404(Apartment, number=apartment_number)

    # Pass the apartment object to the template
    return render(request, 'pagos/apartment_detail.html', {'apartment': apartment})


#------------------------------
#### 3.3 Cotización ###
#------------------------------

def select_apartment_view(request):
    projects = Project.objects.all()
    apartments = None
    selected_apartment = None
    selected_project = None
    selected_price_list = None
    total_price = None

    if request.method == 'POST':
        project_id = request.POST.get('project')
        apartment_number = request.POST.get('apartment_number')

        if project_id:
            selected_project = get_object_or_404(Project, id=project_id)
            apartments = Apartment.objects.filter(project=selected_project)

            if apartment_number:
                selected_apartment = apartments.filter(number=apartment_number).first()

                # Fetch the PriceList for the selected apartment
                if selected_apartment:
                    selected_price_list = PriceList.objects.filter(apartment=selected_apartment).first()
                    total_price = selected_apartment.area * selected_price_list.current_list_price

    return render(request, 'pagos/select_apartment.html', {
        'projects': projects,
        'apartments': apartments,
        'selected_apartment': selected_apartment,
        'selected_project': selected_project,
        'selected_price_list': selected_price_list,
        'total_price': total_price,
    })


# -------------------------------

def calcular_plan_pagos(precio_lista, porcentaje_enganche, porcentaje_descuento, porcentaje_mensualidades, num_mensualidades, mes_inicio):
    """Calculates the payment plan based on various parameters."""
    
    # Ensure precio_lista is a Decimal
    precio_lista = Decimal(precio_lista)

    # Calculate total percentages for payments
    porcentaje_pago_final = Decimal(100) - porcentaje_enganche - porcentaje_mensualidades 
    precio_descuento = precio_lista * (Decimal(1) - porcentaje_descuento / Decimal(100))
    
    # Calculate payments
    enganche = precio_descuento * (porcentaje_enganche / Decimal(100))
    pago_mensual = precio_descuento * (porcentaje_mensualidades / Decimal(100)) / Decimal(num_mensualidades)
    pago_final = precio_descuento * (porcentaje_pago_final / Decimal(100))
    
    # Generate payment schedule
    pagos = []
    current_date = mes_inicio

    # Add enganche payment
    pagos.append({'mes': current_date.strftime('%B %Y'), 'pago': float(enganche), 'tipo': 'Enganche'})

    # Add monthly payments
    for _ in range(num_mensualidades):
        last_day = calendar.monthrange(current_date.year, current_date.month)[1]
        current_date += timedelta(days=last_day)
        pagos.append({'mes': current_date.strftime('%B %Y'), 'pago': float(pago_mensual), 'tipo': 'Mensualidad'})

    # Add final payment
    last_day = calendar.monthrange(current_date.year, current_date.month)[1]
    current_date += timedelta(days=last_day)
    pagos.append({'mes': current_date.strftime('%B %Y'), 'pago': float(pago_final), 'tipo': 'Pago final'})

    # Compile payment plan
    plan_pagos = {
        'pagos': pagos,
        'total': float(enganche + (pago_mensual * Decimal(num_mensualidades)) + pago_final),
    }

    return plan_pagos

# -------------------------------
from django.core.mail import send_mail
from django.conf import settings

def payment_plan_view(request):
    from decimal import Decimal
    total_price = request.GET.get('total_price')
    apartment_number = request.GET.get('apartment_number')
    selected_project_name = request.GET.get('selected_project')

    if total_price:
        total_price = Decimal(total_price)

    apartment = Apartment.objects.filter(number=apartment_number).first()
    project = Project.objects.filter(name=selected_project_name).first()

    if not apartment or not project:
        return render(request, 'pagos/plan_pagos.html', {
            'error': 'Invalid apartment or project selected.'
        })

    form = PaymentPlanForm(request.POST or None)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'calculate' and form.is_valid():
            data = form.cleaned_data
            mes_inicio = data['mes_inicio']
            plan_pagos = calcular_plan_pagos(
                total_price,
                data['porcentaje_enganche'],
                data['porcentaje_descuento'],
                data['porcentaje_mensualidades'],
                data['num_mensualidades'],
                mes_inicio
            )

            npv = calculate_npv(plan_pagos['pagos'], 0.05)
            npv = Decimal(npv) if isinstance(npv, float) else npv
            ratio = npv / total_price if npv > 0 else None
            indicator_color = 'green' if ratio and ratio >= 0.95 else 'yellow' if ratio and ratio >= 0.90 else 'red'

            return render(request, 'pagos/plan_pagos.html', {
                'form': form,
                'plan_pagos': plan_pagos,
                'npv': npv,
                'indicator_color': indicator_color,
                'ratio': ratio,
            })

        elif action == 'cotizacion' and form.is_valid():
            data = form.cleaned_data
            mes_inicio = data['mes_inicio']
            plan_pagos = calcular_plan_pagos(
                total_price,
                data['porcentaje_enganche'],
                data['porcentaje_descuento'],
                data['porcentaje_mensualidades'],
                data['num_mensualidades'],
                mes_inicio
            )

            cliente_id = data['cliente'].id_cliente  # Assuming 'cliente' field is the selected client
            cliente = Cliente.objects.get(id_cliente=cliente_id)
            cliente_email = cliente.get_email()

            total_price = request.GET.get('total_price')
            apartment_number = request.GET.get('apartment_number')
            selected_project_name = request.GET.get('selected_project')

            # Convert total_price to a Decimal for formatting purposes
            from decimal import Decimal
            if total_price:
                total_price = Decimal(total_price)

            # Define subject and format the message
            # Define subject with project name and apartment number
            subject = f"Cotización del {selected_project_name} - Apartamento {apartment_number}"
            email_message = f"""
Estimado cliente,

Aquí está su cotización para el proyecto **{selected_project_name}** y el apartamento **{apartment_number}** con precio total: ${total_price:,.2f}.

Resultados del Plan de Pagos:
"""

            for pago in plan_pagos['pagos']:
                email_message += f"Mes {pago['mes']} - {pago['tipo']} - ${pago['pago']:.2f}\n"

            email_message += f"\nTotal a Pagar: ${plan_pagos['total']:.2f}\n"
            email_message += "\nAtentamente,\nEl equipo de ventas"

            # Send the email
            send_mail(
                subject=subject,
                message=email_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[cliente_email],
                fail_silently=False,
            )

            return render(request, 'pagos/index.html', {
                'message': 'Cotización enviada al cliente exitosamente.'
            })

    return render(request, 'pagos/plan_pagos.html', {
        'form': form,
        'total_price': total_price,
        'apartment_number': apartment_number,
        'selected_project': selected_project_name,
    })





#------------------------------------
#### 3.4 Proceso de venta o apartado ###
#------------------------------------
def review_apartments_view(request):
    projects = Project.objects.prefetch_related('apartments').all()  # Fetch all projects and related apartments

    return render(request, 'pagos/review_apartments.html', {
        'projects': projects,
    })

#------------------------------------

def apartar(request, apartment_id):
    # Fetch the apartment, or return 404 if it doesn't exist
    apartment = get_object_or_404(Apartment, id=apartment_id)

    if request.method == 'POST':
        # Update apartment status to "apartado" (reserved)
        apartment.status = 'apartado'
        apartment.save()  # Save the updated status to the database

        # Redirect to the list of apartments or an appropriate view
        return redirect('lista_departamentos')  # Make sure this URL name exists in urls.py

    # Render the confirmation page for reservation
    return render(request, 'pagos/apartar.html', {
        'apartment': apartment,
    })
# -------------------------------

def disponible_view(request,apartment_id):
    # Fetch the apartment, or return 404 if it doesn't exist
    apartment = get_object_or_404(Apartment, id=apartment_id)

    if request.method == 'POST':
        # Update apartment status to "apartado" (reserved)
        apartment.status = 'disponible'
        apartment.save()  # Save the updated status to the database

        # Redirect to the list of apartments or an appropriate view
        return redirect('lista_departamentos')  # Make sure this URL name exists in urls.py

    # Render the confirmation page for reservation
    return render(request, 'pagos/disponible.html', {
        'apartment': apartment,
})

# -------------------------------

def ventas(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id)
    project = apartment.project  # Retrieve the project once
    plan_pagos = None  # Initialize payment plan variable
    error_message = None  # Initialize error message variable

    # Create an instance of PaymentPlanForm
    payment_plan_form = PaymentPlanForm(request.POST or None)

    if request.method == 'POST':
        # Handle payment form submission
        if payment_plan_form.is_valid():
            # Access cleaned data only after validation
            cliente = payment_plan_form.cleaned_data['cliente']
            porcentaje_descuento = payment_plan_form.cleaned_data['porcentaje_descuento']
            porcentaje_enganche = payment_plan_form.cleaned_data['porcentaje_enganche']
            porcentaje_mensualidades = payment_plan_form.cleaned_data['porcentaje_mensualidades']
            num_mensualidades = payment_plan_form.cleaned_data['num_mensualidades']
            mes_inicio = payment_plan_form.cleaned_data['mes_inicio']

            # Calculate the payment plan
            precio_lista = apartment.total_price  # Assuming `apartment.total_price` exists
            
            try:
                plan_pagos = calcular_plan_pagos(
                    precio_lista, 
                    porcentaje_enganche, 
                    porcentaje_descuento, 
                    porcentaje_mensualidades, 
                    num_mensualidades, 
                    mes_inicio
                )

                # Create a new PaymentRecord with the calculated plan
                PaymentRecord.objects.create(
                    cliente=cliente,
                    apartment=apartment,
                    project=project,
                    porcentaje_descuento=porcentaje_descuento,
                    porcentaje_enganche=porcentaje_enganche,
                    porcentaje_mensualidades=porcentaje_mensualidades,
                    num_mensualidades=num_mensualidades,
                    mes_inicio=mes_inicio,
                    payment_schedule=plan_pagos['pagos']  # Save the calculated plan
                )

                # Update the apartment status to "Vendido"
                apartment.status = "vendido"
                apartment.save()  # Save the updated apartment status

                return redirect('pagos:list_payment_records')  # Redirect after saving

            except ValueError as e:
                error_message = str(e)  # Capture the error message

    return render(request, 'pagos/venta.html', {
        'apartment': apartment,
        'project': project,
        'plan_pagos': plan_pagos,
        'error_message': error_message,  # Pass error message to the template
        'payment_plan_form': payment_plan_form,  # Pass the form to the template
    })



def save_payment_record(request, form, apartment, project, payment_schedule):
    # Convert Decimal values in payment_schedule to float
    for payment in payment_schedule:
        payment['pago'] = float(payment['pago'])  # Convert to float

    data = form.cleaned_data
    cliente = data['cliente']

    # Create a new PaymentRecord instance
    payment_record = PaymentRecord(
        cliente=cliente,
        apartment=apartment,
        project=project,
        porcentaje_descuento=form.cleaned_data['porcentaje_descuento'],
        porcentaje_enganche=form.cleaned_data['porcentaje_enganche'],
        porcentaje_mensualidades=form.cleaned_data['porcentaje_mensualidades'],
        num_mensualidades=form.cleaned_data['num_mensualidades'],
        mes_inicio=form.cleaned_data['mes_inicio'],
        payment_schedule=payment_schedule  # Save the payment schedule here
    )
    payment_record.save()
    return True


# -------------------------------
#### 3.6 Pagos y estado de cuenta $$$
# -------------------------------

"""
def list_payment_records(request):
    records = PaymentRecord.objects.all()
    return render(request, 'pagos/payment_records_list.html', {'records': records})

"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import PaymentRecord

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def list_payment_records(request):
    is_admin = request.user.is_superuser or request.user.groups.filter(name='Administrador').exists()

    # Check if the user is a superuser
    if request.user.is_superuser:
        # If the user is a superuser, allow access to all records
        records = PaymentRecord.objects.all()
    else:
        try:
            # Get the logged-in user's Cliente profile
            cliente = request.user.cliente_profile
            # If Cliente exists, fetch their payment records
            records = PaymentRecord.objects.filter(cliente=cliente)
        except Cliente.DoesNotExist:
            # If no Cliente profile is found, redirect to a page to create the profile
            messages.error(request, "You do not have a Cliente profile. Please complete your profile.")
            return redirect('payments_index')  # Redirect to the page where the user can create a Cliente profile

    # Render the payment records page
    return render(request, 'pagos/payment_records_list.html',{'records': records, 'is_admin': is_admin})


# -------------------------------

def record_detail_view(request, pk):
    record = get_object_or_404(PaymentRecord, pk=pk)
    return render(request, 'pagos/payment_record_detail.html', {'record': record})

# -------------------------------

def delete_record(request, id):
    record = get_object_or_404(PaymentRecord, id=id)
    if request.method == 'POST':
        record.delete()
        messages.success(request, 'Record deleted successfully.')
    return redirect('list_payment_records')  # Replace with the name of your listing view

# -------------------------------

from django.shortcuts import get_object_or_404, render, redirect
from datetime import datetime
from bancos.models import Transaction, BankAccount  # Import the relevant models
from pagos.models import PaymentRecord  # Assuming PaymentRecord is your payment model

def register_payment(request, payment_record_id):
    # Retrieve the PaymentRecord using its ID
    payment_record = get_object_or_404(PaymentRecord, id=payment_record_id)

    # Retrieve the associated Project for the PaymentRecord
    project = payment_record.project

    if request.method == 'POST':
        # Retrieve the amount paid from the form submission
        amount_paid = request.POST.get('amount_paid')
        amount_paid = Decimal(request.POST.get('amount_paid'))

        # Create the PaymentTransaction (this will be your payment record)
        payment_transaction = PaymentTransaction.objects.create(
            payment_record=payment_record,
            amount_paid=amount_paid,
            payment_date=datetime.today().date(),
        )

        # Retrieve the associated BankAccount from the Project
        
        bank_account = project.bank_accounts.first()  # Assuming there's only one BankAccount per Project
        
        if bank_account:  # Check if the BankAccount exists
            # Create a Deposit Transaction in the bancos app
            bank_account.deposit(amount_paid, description=f"Payment for {payment_record.cliente}'s apartment {payment_record.apartment}")
                        
            Transaction.objects.create(
                bank_account=bank_account,
                amount=amount_paid,
                transaction_type=Transaction.DEPOSIT,  # Since the payment is a deposit
                description=f"Payment for {payment_record.cliente}'s apartment {payment_record.apartment}"
            )
        else:
            # Handle the case where no BankAccount is found for the Project
            print("No BankAccount found for the project.")

        # Redirect to the list of payment records after successful payment registration
        return redirect('pagos:list_payment_records')

    # If it's a GET request, render the form to register the payment
    return render(request, 'pagos/register_payment.html', {
        'payment_record': payment_record,
    })


# -------------------------------

def account_statement(request, payment_record_id):
    # Obtener el registro de pago directamente
    payment_record = get_object_or_404(PaymentRecord, id=payment_record_id)

    # Crear o recuperar el estado de cuenta asociado
    account_statement, created = AccountStatement.objects.get_or_create(payment_record=payment_record)

    # Sumar todos los pagos programados en el payment_schedule
    total_due = sum(payment['pago'] for payment in payment_record.payment_schedule)

    # Asignar el total calculado a account_statement.total_due y guardar
    account_statement.total_due = total_due
    account_statement.save()

    # Calcular totales si es necesario (asegúrate de que calculate_totals no sobrescriba total_due)
    account_statement.calculate_totals()

    # Contexto para la plantilla
    context = {
        'payment_record': payment_record,
        'account_statement': account_statement,
        'transactions': payment_record.transactions.all(),
        'payment_schedule': payment_record.payment_schedule,  # Acceso directo a payment_schedule
    }

    return render(request, 'pagos/account_statement.html', context)

# -------------------------------
#### Otros ###
# -------------------------------

def cliente_list_view(request):
    clientes_queryset = Cliente.objects.all()
    clientes = [ListaCliente(cliente) for cliente in clientes_queryset]
    return render(request, 'pagos/lista_clientes.html', {'clientes': clientes})

# -------------------------------

from django.views import View
from django.http import JsonResponse

class CalculateNPVView(View):
    def get(self, request, payment_record_id, *args, **kwargs):
        # Get the PaymentRecord instance
        payment_record = get_object_or_404(PaymentRecord, id=payment_record_id)
        
        # Retrieve the payment schedule and define the discount rate
        payment_schedule = payment_record.payment_schedule
        print(payment_schedule)
        discount_rate = 0.05  # Example: 5% annual discount rate

        # Calculate NPV
        npv = calculate_npv(payment_schedule, discount_rate)

        # Return NPV in JSON response
        return JsonResponse({'npv': npv})

from datetime import datetime
from dateutil.relativedelta import relativedelta


def calculate_npv(payment_schedule, discount_rate):
    # Convert discount rate to a monthly rate
    monthly_discount_rate = (1 + discount_rate) ** (1/12) - 1
    
    # Determine the start date for calculating periods
    try:
        start_date = datetime.strptime(payment_schedule[0].get('mes', ''), "%B %Y")
    except (IndexError, ValueError, TypeError):
        return "Error: 'mes' date format issue in payment schedule."
    
    npv = 0.0
    
    for payment_entry in payment_schedule:
        # Safely get values from the dictionary with defaults if missing
        payment_date_str = payment_entry.get('mes')
        payment_amount = payment_entry.get('pago', 0)
        
        # Skip entries where 'mes' or 'pago' is missing
        if payment_date_str is None or payment_amount is None:
            continue
        
        # Parse the payment date
        try:
            payment_date = datetime.strptime(payment_date_str, "%B %Y")
        except ValueError:
            continue  # Skip this entry if date parsing fails
        
        # Calculate the period in months from the start date
        period = (payment_date.year - start_date.year) * 12 + (payment_date.month - start_date.month)
        
        # Add discounted payment to NPV
        npv += payment_amount / ((1 + monthly_discount_rate) ** period)
    
    return npv

