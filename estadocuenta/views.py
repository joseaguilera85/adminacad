from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DeleteView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from django.utils import timezone
from datetime import timedelta


from django.db import models
from .models import BankAccountMovement
from .forms import BankAccountMovementForm
from adminacad.models import Student

def estadocuenta(request):
    # Add any necessary context data here
    context = {}
    return render(request, 'portada_estadocuenta.html', context)

class BankAccountMovementListView(ListView):
    model = BankAccountMovement
    template_name = 'bankaccountmovement_list.html'


class BankAccountMovementStudentListView(ListView):
    model = BankAccountMovement
    template_name = 'bankaccountmovement_list.html'

    def get_queryset(self):
        # Get the student ID from the URL
        identificacion = self.kwargs['identificacion']

        # Filter movements by the student ID
        queryset = super().get_queryset().filter(student__identificacion=identificacion).order_by('transaction_date')

        return queryset

    def get_balance(self):
        """
        Returns the current balance of the account based on the sum of all deposits and withdrawals.
        """
        identificacion = self.kwargs['identificacion']
        # Get all the deposit amounts for the account
        deposits = self.model.objects.filter(student__identificacion=identificacion, transaction_type__in=['A', 'B', 'C'], transaction_date__lte=timezone.now().date()).aggregate(total=models.Sum('amount'))['total'] or 0
        # Get all the withdrawal amounts for the account
        withdrawals = self.model.objects.filter(student__identificacion=identificacion, transaction_type__in=['D', 'E', 'F'], transaction_date__lte=timezone.now().date()).aggregate(total=models.Sum('amount'))['total'] or 0
        # Calculate the balance by subtracting the total withdrawals from the total deposits
        balance = deposits - withdrawals
        return balance
    
    def get_balance_col(self):
        """
        Returns the current balance of the account based on the sum of all deposits and withdrawals.
        """
        identificacion = self.kwargs['identificacion']
        # Get all the deposit amounts for the account
        deposits = self.model.objects.filter(student__identificacion=identificacion,transaction_type='A', transaction_date__lte=timezone.now().date()).aggregate(total=models.Sum('amount'))['total'] or 0
        # Get all the withdrawal amounts for the account
        withdrawals = self.model.objects.filter(student__identificacion=identificacion, transaction_type='D', transaction_date__lte=timezone.now().date()).aggregate(total=models.Sum('amount'))['total'] or 0
        # Calculate the balance by subtracting the total withdrawals from the total deposits
        balance_col= deposits - withdrawals
        return balance_col

    def get_balance_cuo(self):
        """
        Returns the current balance of the account based on the sum of all deposits and withdrawals.
        """
        identificacion = self.kwargs['identificacion']
        # Get all the deposit amounts for the account
        deposits = self.model.objects.filter(student__identificacion=identificacion,transaction_type='C').aggregate(total=models.Sum('amount'))['total'] or 0
        # Get all the withdrawal amounts for the account
        withdrawals = self.model.objects.filter(student__identificacion=identificacion, transaction_type='F').aggregate(total=models.Sum('amount'))['total'] or 0
        # Calculate the balance by subtracting the total withdrawals from the total deposits
        balance_cuo= deposits - withdrawals
        return balance_cuo

    def get_balance_seg(self):
        """
        Returns the current balance of the account based on the sum of all deposits and withdrawals.
        """
        identificacion = self.kwargs['identificacion']
        # Get all the deposit amounts for the account
        deposits = self.model.objects.filter(student__identificacion=identificacion,transaction_type='B').aggregate(total=models.Sum('amount'))['total'] or 0
        # Get all the withdrawal amounts for the account
        withdrawals = self.model.objects.filter(student__identificacion=identificacion, transaction_type='E').aggregate(total=models.Sum('amount'))['total'] or 0
        # Calculate the balance by subtracting the total withdrawals from the total deposits
        balance_seg= deposits - withdrawals
        return balance_seg

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['balance'] = self.get_balance()
        context['balance_col'] = self.get_balance_col()
        context['balance_cuo'] = self.get_balance_cuo()
        context['balance_seg'] = self.get_balance_seg()
        return context


class BankAccountMovementCreateView(CreateView):
    model = BankAccountMovement
    form_class = BankAccountMovementForm
    template_name = 'bankaccountmovement_form.html'
    success_url = reverse_lazy('movimientos_list')

    def form_valid(self, form):
        # Get the identificacion from the form data
        identificacion = form.cleaned_data['identificacion']

        # Get the student object based on the identificacion
        student = get_object_or_404(Student, identificacion=identificacion)

        # Set the student object on the BankAccountMovement instance
        form.instance.student = student

        return super().form_valid(form)

class BankAccountMovementDeleteView(DeleteView):
    model = BankAccountMovement
    success_url = reverse_lazy('movimientos_list')
    template_name = 'confirm_delete.html'


from django.db import connection
from django.http import HttpResponse

def add_movement(request, identificacion):
    student = get_object_or_404(Student, identificacion=identificacion)
    bank_account = BankAccountMovement.objects.get(student=student)
    context = {'student': student, 'bank_account': bank_account}
    return render(request, 'add_movement.html', context)

def execute_sql(request, identificacion):
    student = get_object_or_404(Student, identificacion=identificacion)
    with connection.cursor() as cursor:
        cursor.execute(f"""
INSERT INTO estadocuenta_bankaccountmovement (transaction_date, transaction_type, amount, description, student_id)
VALUES ('2023-01-01', 'A', 2000, 'Colegiatura Enero', {student.pk}),
       ('2023-02-01', 'A', 2000, 'Colegiatura Febrero', {student.pk}),
       ('2023-03-01', 'A', 2000, 'Colegiatura Marzo', {student.pk}),
       ('2023-04-01', 'A', 2000, 'Colegiatura Abril', {student.pk}),
       ('2023-05-01', 'A', 2000, 'Colegiatura Mayo', {student.pk});
        """)
        return HttpResponse("SQL code executed successfully.")