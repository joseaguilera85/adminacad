from django.urls import path
from .views import ProjectCreateView, ProjectListView, ProjectUpdateView, ProjectDeleteView # Import ProjectCreateView and other views
from . import views

app_name = 'apartments'

urlpatterns = [
    path('', ProjectListView.as_view(), name='project_list'),
    
    path('projects/', ProjectListView.as_view(), name='project_list'),
    path('create-project/', ProjectCreateView.as_view(), name='create_project'),
    path('project/<int:pk>/edit/', ProjectUpdateView.as_view(), name='project_edit'),
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),    
    
    path('apartments/', views.apartment_list, name='apartment_list'),
    path('apartments/<int:project_id>/', views.apartment_list, name='apartment_list'),  # Filtered by project

    path('add_apartment/', views.apartment_add, name='add_apartment'),
    path('edit/<int:pk>/', views.apartment_edit, name='apartment_edit'),
    path('delete/<int:pk>/', views.apartment_delete, name='apartment_delete'), 
    path('upload/', views.apartment_upload, name='apartment_upload'),
]
