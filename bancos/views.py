# bancos/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse
from .models import BankAccount
from .forms import DepositForm, WithdrawForm

def bancos_menu(request):
    return render(request, 'bancos/bancos_menu.html')





def account_transactions(request, account_number):
    account = get_object_or_404(BankAccount, account_number=account_number)
    transactions = account.transactions.all()  # Get all transactions for this account
    project_name = account.project.name  # Access the project name
    print (project_name)

    return render(
        request,
        'bancos/account_transactions.html',
        {
            'account': account,
            'transactions': transactions,
            'project_name': project_name,  # Pass project name to the template
        }
    )



def deposit(request, account_number):
    bank_account = get_object_or_404(BankAccount, account_number=account_number)
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            description = form.cleaned_data['description']
            bank_account.deposit(amount, description)
            return redirect(reverse('bancos:account_transactions', args=[account_number]))
    else:
        form = DepositForm()
    return render(request, 'bancos/deposit.html', {'form': form, 'bank_account': bank_account})

def withdraw(request, account_number):
    bank_account = get_object_or_404(BankAccount, account_number=account_number)
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            description = form.cleaned_data['description']
            try:
                bank_account.withdraw(amount, description)
                return redirect(reverse('bancos:account_transactions', args=[account_number]))
            except ValueError as e:
                form.add_error('amount', str(e))
    else:
        form = WithdrawForm()
    return render(request, 'bancos/withdraw.html', {'form': form, 'bank_account': bank_account})


def bank_account_list(request):
    # Fetch all bank accounts
    bank_accounts = BankAccount.objects.all()

    # Pass the bank accounts to the template
    return render(request, 'bancos/bank_account_list.html', {'bank_accounts': bank_accounts})