# bancos/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from apartments.models import Project  # Import Project model
from .models import BankAccount  # Import BankAccount model

@receiver(post_save, sender=Project)
def create_bank_account_for_project(sender, instance, created, **kwargs):
    if created:  # Only create a bank account when the project is newly created
        # Create a new BankAccount for the newly created project
        BankAccount.objects.create(
            account_number=f"ACC-{instance.id}",  # You can create an account number based on the project ID
            project=instance  # Link the account to the newly created project
        )
