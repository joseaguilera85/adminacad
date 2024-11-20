from django.urls import path
from . import views
from .views import BankAccountMovementListView, BankAccountMovementCreateView, BankAccountMovementStudentListView, BankAccountMovementDeleteView, estadocuenta, execute_sql
from .views import execute_sql, add_movement

urlpatterns = [
    path('', estadocuenta, name='estadocuenta'),
    path('movimientos/', BankAccountMovementListView.as_view(), name='movimientos_list'),
    path('movimientos/<int:identificacion>', BankAccountMovementStudentListView.as_view(), name='movimientos_studentlist'),
    path('create-movement/', BankAccountMovementCreateView.as_view(), name='bankaccountmovementform'),
    path('carga/<int:identificacion>/', add_movement, name='cargamov'),
    path('movimientos/delete/<int:pk>/', BankAccountMovementDeleteView.as_view(), name='movimientos_delete'),
    
    path('execute-sql/<int:identificacion>/', execute_sql, name='execute_sql')

]