# project/urls.py or app/urls.py
from django.contrib.auth.views import LoginView
from . import views
from django.urls import path
from .views import register_user, send_email_view
from .views import CustomPasswordChangeView

app_name = 'menu'

urlpatterns = [
    # Other URLs ...
    path('', views.menu, name='menu'),
    path('login/', LoginView.as_view(template_name='menu/login.html'), name='login'),
    path('menu/', views.menu, name='menu'),
    
    
    path("register_clientes/", views.register_clientes, name="register_clientes"),
    path("register/", register_user, name="register_user"),
    
    
    path('change-password/', CustomPasswordChangeView.as_view(), name='change_password'),
    path('send-email/', send_email_view, name='send_email')

]
