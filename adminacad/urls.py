from django.urls import path
from .views import *
from . import views

urlpatterns = [

    #path('', IndexView.as_view(), name='index'),
    path('index/', intro, name='index'),
    path('menu/', menu, name='menu'),
    path('login/', login_view, name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),

    path('salones/', SalonesListView.as_view(), name='salones_list'),
    path('salones/create/', SalonesCreateView.as_view(), name='salones_create'),
    path('salones/<int:pk>/', SalonesDetailView.as_view(), name='salones_detail'),
    path('salones/update/<int:pk>', SalonesUpdateView.as_view(), name='salones_update'),
    path('salones/delete/<int:pk>/', SalonesDeleteView.as_view()),


    path('student/', StudentListView.as_view(), name='student_list'),
    path('student/create/', StudentCreateView.as_view(), name='student_create'),
    path('student/<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('student/update/<int:pk>/', StudentUpdateView.as_view(), name='student_update'),
    path('student/delete/<int:pk>/', StudentDeleteView.as_view(), name='student_delete'),

    path('studentmateria/<str:materia_clave>/', views.studentmateria, name='studentmateria'),


    path('materias/', views.MateriasListView.as_view(), name='materias_list'),
    path('materias/create/', views.MateriasCreateView.as_view(), name='materias_create'),
    path('materias/edit/<int:pk>/', views.MateriasUpdateView.as_view(), name='materias_edit'),
    path('materias/delete/<int:pk>/', views.MateriasDeleteView.as_view(), name='materias_delete'),


    path('calificacion/', views.calificacion_list, name='calificacion_list'),
    path('calificacion/<int:pk>/', views.calificacion_detail, name='calificacion_detail'),
    path('calificacion/new/', views.calificacion_new, name='calificacion_new'),
    path('calificacion/edit/<int:pk>/', views.calificacion_edit, name='calificacion_edit'),
    path('calificacion/delete/<int:pk>/', views.calificacion_delete, name='calificacion_delete'),
]
