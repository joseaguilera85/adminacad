#---------------------------
# views.py

# Import necessary modules
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from .forms import UserRegistrationForm, ClienteRegistrationForm
from clientes.models import Cliente


# Menu view for authenticated users, checking user groups
@login_required
def menu(request):
    # Check the groups the user belongs to
    is_ventas_group = request.user.groups.filter(name='Ventas').exists()
    is_clientes_group = request.user.groups.filter(name='Cliente').exists()
    is_administracion_group = request.user.groups.filter(name='Administracion').exists()
    
    # Pass these variables to the context for rendering
    context = {
        'is_ventas_group': is_ventas_group,
        'is_clientes_group': is_clientes_group,
        'is_administracion_group': is_administracion_group,
        # Add any other necessary context variables here
    }
    
    # Render the menu page with the context
    return render(request, 'menu/menu.html', context)


#---------------------------


# User registration view
def register_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to the menu after successful registration
            return redirect("menu:menu")
    else:
        form = UserRegistrationForm()

    # Render the registration page with the form
    return render(request, "menu/register_user.html", {"form": form})


#---------------------------


# Client registration view, filtering available clients without users
def register_clientes(request):
    # Filter clients who don't already have a user associated
    available_clients = Cliente.objects.exclude(mail__in=User.objects.values_list('username', flat=True))

    # If no clients are available for registration, display a message
    if not available_clients.exists():
        return render(request, "menu/register_clientes.html", {"message": "No clients available for registration."})

    if request.method == "POST":
        form = ClienteRegistrationForm(request.POST)
        if form.is_valid():
            try:
                form.save()  # Save the new client data
                return redirect("menu:menu")  # Redirect after successful registration
            except IntegrityError:
                # Handle the error if the user already exists
                form.add_error(None, "A user with the selected client's email already exists.")
    else:
        form = ClienteRegistrationForm()

    # Render the client registration page with the form
    return render(request, "menu/register_clientes.html", {"form": form})


#---------------------------


# Custom password change view
@method_decorator(login_required, name='dispatch')
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'menu/change_password.html'  # Template for changing password
    success_url = reverse_lazy('menu:menu')  # Redirect after password change


#---------------------------


# View to send email from the application
def send_email_view(request):
    if request.method == "POST":
        # Extract data from the form
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        recipient = request.POST.get('recipient')

        # Send the email using the Django send_mail function
        send_mail(
            subject,
            message,
            None,  # Default 'from' address
            [recipient],  # Recipient email address
            fail_silently=False,  # Ensure errors are raised if mail fails
        )

        # Return a response indicating the email was sent
        return HttpResponse("Email sent successfully!")
    
    # Render the email sending form if the request is not POST
    return render(request, 'send_email.html')


#---------------------------


from django.http import JsonResponse
from .utils import send_whatsapp_message  # Assuming the function is in a `utils.py` file

def send_whatsapp_message(request):
    if request.method == "POST":  # Ensure the request is POST
        try:
            result = send_whatsapp_message()
            return JsonResponse({"success": True, "message": result})
        except Exception as error:
            return JsonResponse({"success": False, "error": str(error)})
    return JsonResponse({"success": False, "error": "Invalid request method"})
