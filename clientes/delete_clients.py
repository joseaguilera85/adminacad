# clientes/management/commands/delete_clients.py

from django.core.management.base import BaseCommand
from clientes.models import Client

class Command(BaseCommand):
    help = 'Delete all clients from the database'

    def handle(self, *args, **options):
        Client.objects.all().delete()  # Deletes all clients
        self.stdout.write(self.style.SUCCESS('Successfully deleted all clients'))
