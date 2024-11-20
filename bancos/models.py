# bancos/models.py

from django.db import models
from apartments.models import Project  # Import the Project model

class BankAccount(models.Model):
    account_number = models.CharField(max_length=20, unique=True)  # Unique account number
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)  # Account balance
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='bank_accounts')  # Foreign key to Project

    def __str__(self):
        return f"Account: {self.account_number} - Balance: ${self.balance} - Project: {self.project.name}"

    def deposit(self, amount, description=''):
        """Adds the specified amount to the account balance and logs the transaction."""
        self.balance += amount
        self.save()
        # Create a deposit transaction
        Transaction.objects.create(
            bank_account=self,
            amount=amount,
            transaction_type=Transaction.DEPOSIT,
            description=description
        )

    def withdraw(self, amount, description=''):
        """Subtracts the specified amount from the account balance if funds are sufficient and logs the transaction."""
        if amount <= self.balance:
            self.balance -= amount
            self.save()
            # Create a withdrawal transaction
            Transaction.objects.create(
                bank_account=self,
                amount=amount,
                transaction_type=Transaction.WITHDRAWAL,
                description=description
            )
        else:
            raise ValueError("Insufficient funds for this withdrawal.")
            

class Transaction(models.Model):
    DEPOSIT = 'deposit'
    WITHDRAWAL = 'withdrawal'
    
    TRANSACTION_TYPE_CHOICES = [
        (DEPOSIT, 'Deposit'),
        (WITHDRAWAL, 'Withdrawal'),
    ]
    
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='transactions')  # ForeignKey to BankAccount
    amount = models.DecimalField(max_digits=12, decimal_places=2)  # Transaction amount
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)  # Type of transaction
    description = models.CharField(max_length=255, blank=True, null=True)  # Optional description
    date = models.DateTimeField(auto_now_add=True)  # Date and time of the transaction
    
    def __str__(self):
        return f"{self.transaction_type.capitalize()} of ${self.amount} on {self.date.strftime('%Y-%m-%d %H:%M:%S')}"
