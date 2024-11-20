from django.core.management.base import BaseCommand
from clientes.models import Cliente, Project
from datetime import datetime, timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate Cliente records with dummy data'

    def handle(self, *args, **kwargs):
        # Create the Montaura project
        montaura_project = Project.objects.create(name="EGL")

        # Calculate one month ago
        one_month_ago = timezone.now() - timedelta(days=30)

        # Sample Cliente records with created_at set to one month ago
        clientes = [
    {"user": None, "nombre": "Ella", "apellido": "Miller", "edad": 28, "celular": "3216549870", "mail": "ella.miller@example.com", "project": montaura_project, "modo_contacto": "redes", "estatus": "lead", "tipo_propiedad": "terreno", "created_at": one_month_ago},
    {"user": None, "nombre": "James", "apellido": "Anderson", "edad": 45, "celular": "4327650981", "mail": "james.anderson@example.com", "project": montaura_project, "modo_contacto": "fisico", "estatus": "lead", "tipo_propiedad": "departamento", "created_at": one_month_ago},
    {"user": None, "nombre": "Grace", "apellido": "Taylor", "edad": 34, "celular": "5438762098", "mail": "grace.taylor@example.com", "project": montaura_project, "modo_contacto": "redes", "estatus": "lead", "tipo_propiedad": "casa", "created_at": one_month_ago},
    {"user": None, "nombre": "Benjamin", "apellido": "Harris", "edad": 40, "celular": "6549873201", "mail": "benjamin.harris@example.com", "project": montaura_project, "modo_contacto": "fisico", "estatus": "lead", "tipo_propiedad": "terreno", "created_at": one_month_ago},
    {"user": None, "nombre": "Lily", "apellido": "Martin", "edad": 26, "celular": "7650984321", "mail": "lily.martin@example.com", "project": montaura_project, "modo_contacto": "redes", "estatus": "lead", "tipo_propiedad": "departamento", "created_at": one_month_ago},
    {"user": None, "nombre": "William", "apellido": "Scott", "edad": 50, "celular": "8765432109", "mail": "william.scott@example.com", "project": montaura_project, "modo_contacto": "fisico", "estatus": "lead", "tipo_propiedad": "casa", "created_at": one_month_ago},
    {"user": None, "nombre": "Amelia", "apellido": "Carter", "edad": 30, "celular": "9876543210", "mail": "amelia.carter@example.com", "project": montaura_project, "modo_contacto": "redes", "estatus": "lead", "tipo_propiedad": "terreno", "created_at": one_month_ago},
    {"user": None, "nombre": "Alexander", "apellido": "Davis", "edad": 37, "celular": "1357924680", "mail": "alexander.davis@example.com", "project": montaura_project, "modo_contacto": "fisico", "estatus": "lead", "tipo_propiedad": "departamento", "created_at": one_month_ago},
    {"user": None, "nombre": "Charlotte", "apellido": "Lopez", "edad": 32, "celular": "2468135790", "mail": "charlotte.lopez@example.com", "project": montaura_project, "modo_contacto": "redes", "estatus": "lead", "tipo_propiedad": "casa", "created_at": one_month_ago},
    {"user": None, "nombre": "Lucas", "apellido": "King", "edad": 43, "celular": "3579246801", "mail": "lucas.king@example.com", "project": montaura_project, "modo_contacto": "fisico", "estatus": "lead", "tipo_propiedad": "terreno", "created_at": one_month_ago}
]


        # Create Cliente records
        for cliente_data in clientes:
            Cliente.objects.create(**cliente_data)

        self.stdout.write(self.style.SUCCESS('Successfully populated Cliente records'))
