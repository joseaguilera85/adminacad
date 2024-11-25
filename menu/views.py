# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def menu(request):
    is_ventas_group = request.user.groups.filter(name='Ventas').exists()
    is_clientes_group = request.user.groups.filter(name='Clientes').exists()
    is_administracion_group = request.user.groups.filter(name='Administracion').exists()
    
    # Add these variables to the context
    context = {
        'is_ventas_group': is_ventas_group,
        'is_clientes_group': is_clientes_group,
        'is_administracion_group': is_administracion_group,
        # other context variables you need to pass
    }
    

    # Pass this information to the template
    return render(request, 'menu/menu.html', context)


#---------------------------

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserRegistrationForm

def register_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("menu:menu")  # Redirect to a success page or login page
    else:
        form = UserRegistrationForm()
    return render(request, "menu/register_user.html", {"form": form})

#---------------------------

from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'menu/change_password.html'
    success_url = reverse_lazy('menu:menu')  # Redirect to a success page


#---------------------------

from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse

def send_email_view(request):
    if request.method == "POST":
        # Get data from the form
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        recipient = request.POST.get('recipient')

        # Send the email
        send_mail(
            subject,
            message,
            None,
            [recipient],
            fail_silently=False,
        )

        # Redirect or display a success message
        return HttpResponse("Email sent successfully!")
    
    return render(request, 'send_email.html')



#-------------------