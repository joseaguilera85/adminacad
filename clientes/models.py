from django.db import models
from apartments.models import Project
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
from django.core.paginator import Paginator

# ----------------------------------------

class Cliente(models.Model):
    id_cliente = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cliente_profile', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_clientes")

    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    edad = models.IntegerField()
    celular = models.CharField(max_length=15)
    mail = models.EmailField()

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='clientes', null=True, blank=True)
    
    modo_contacto = models.CharField(max_length=50, default='N/A', choices=[
        ('redes', 'Redes'),
        ('fisico', 'Fisico'),
    ])
    estatus = models.CharField(max_length=50, choices=[
        ('lead', 'Lead'),
        ('cliente', 'Cliente'),
        ('inactivo', 'Inactivo'),
    ])
    tipo_propiedad = models.CharField(max_length=50, choices=[
        ('terreno', 'Terreno'),
        ('departamento', 'Departamento'),
        ('casa', 'Casa'),
    ])

    # New fields for interactions
    last_interaction = models.DateTimeField(null=True, blank=True)
    interaction_status = models.CharField(
        max_length=50, 
        default='No Interaction', 
        choices=[
            ('Recent', 'Recent'),
            ('Stale', 'Stale'),
            ('No Interaction', 'No Interaction'),
        ]
    )

    # Update interaction details
    def update_interaction_status(self):
        # Get the most recent interaction for this client
        last_interaction = self.interactions.order_by('-date').first()

        if last_interaction:
            self.last_interaction = last_interaction.date
            days_since_last = (timezone.now() - last_interaction.date).days
            self.interaction_status = 'Recent' if days_since_last <= 30 else 'Stale'
        else:
            self.last_interaction = None
            self.interaction_status = 'Prueba'
        
        self.save()

    def get_email(self):
        return self.mail 

    def __str__(self):
        return f"{self.celular} {self.nombre} {self.apellido}"


# ----------------------------------------

class Interaction(models.Model):
    INTERACTION_TYPES = [
        ('Email', 'Email'),
        ('Phone', 'Phone Call'),
        ('Meeting', 'Meeting'),
        ('Other', 'Other'),
    ]
    
    CATEGORIES = [
        ('Follow-up', 'Follow-up'),
        ('Proposal Sent', 'Proposal Sent'),
        ('Contract Signed', 'Contract Signed'),
        ('Other', 'Other'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='interactions')
    salesperson = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.cliente.nombre} - {self.interaction_type} on {self.date.strftime('%Y-%m-%d')}"

# ----------------------------------------

class Meeting(models.Model):
    client = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='meeting')
    apellido = models.CharField(max_length=255)
    salesperson = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Meeting with {self.client.nombre} on {self.date_time.strftime('%Y-%m-%d %H:%M')} by {self.salesperson.username}"

    class Meta:
        unique_together = ('client', 'date_time')
