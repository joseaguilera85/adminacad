# clientes/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import schedule_meeting, meeting_list, edit_meeting, delete_meeting, dashboard_view

app_name = 'clientes'  # This defines the namespace for this app

urlpatterns = [
    path('home/', views.client_home, name='clientes_home'),

    ### 2.O Login ###
    path('', auth_views.LoginView.as_view(template_name='clientes/login.html'), name='login'),  # Use LoginView
    path('login/', auth_views.LoginView.as_view(template_name='clientes/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),  # Use custom logout view

    ### 2.1 Clientes ###
    path('new/', views.new_client, name='new_client'),
    path('consult/', views.consult_clients, name='consult_clients'),
    path('cliente/<uuid:id_cliente>/edit/', views.edit_client, name='edit_client'),  # Add
    path('delete/<uuid:client_id>/', views.delete_client, name='delete_client'),  # Delete client URL
    path('cliente/<uuid:id_cliente>/', views.client_detail, name='client_detail'),
    
    ### 2.2 Interacciones ###
    path('cliente/<uuid:id_cliente>/add_interaction/', views.add_interaction, name='add_interaction'),
    
    ### 2.3 Citas ###
    path('meetings/', meeting_list, name='meeting_list'),  # New URL for meeting list
    path('schedule_meeting/', schedule_meeting, name='schedule_meeting'),
    path('meetings/edit/<int:meeting_id>/', edit_meeting, name='edit_meeting'),  # New URL for editing meetings
    path('meetings/delete/<int:meeting_id>/', delete_meeting, name='delete_meeting'),  # New URL for deleting meetings

    ### 2.4 Dashboard
    path('dashboard/', dashboard_view, name='dashboard'),

    ### 2.5 Eventos
    path('events/create/', views.create_event, name='create_event'), 
    path('events/', views.event_list, name='event_list'),

]

# Global error handler
handler403 = 'clientes.views.custom_403'  # This should be outside of urlpatterns
