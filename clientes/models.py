from django.db import models
from apartments.models import Project
from django.contrib.auth.models import User
import uuid
from django.utils import timezone

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
    
    def get_email(self):
        return self.mail 

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# ----------------------------------------

class Oportunidad(models.Model):
    id_oportunidad = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, related_name='oportunidades')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='oportunidades')
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_oportunidades")
    estatus = models.CharField(max_length=50, choices=[
        ('prospecto', 'Prospecto'),
        ('en_progreso', 'En Progreso'),
        ('cerrado', 'Cerrado'),
    ])

    # New fields for interactions
    last_interaction = models.DateTimeField(null=True, blank=True)
    interaction_status = models.CharField(
        max_length=50, 
        default='No Interaction', 
        choices=[('Recent', 'Recent'),('Stale', 'Stale'),('No Interaction', 'No Interaction')]
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

    def __str__(self):
        return f"{self.cliente.nombre}  {self.project}"



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
    oportunidad = models.ForeignKey(Oportunidad, on_delete=models.CASCADE, related_name='interactions', null=True, blank=True)
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
    oportunidad = models.ForeignKey(Oportunidad, on_delete=models.CASCADE, related_name='meeting', null=True, blank=True)
    apellido = models.CharField(max_length=255)
    salesperson = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Meeting with {self.client.nombre} on {self.date_time.strftime('%Y-%m-%d %H:%M')} by {self.salesperson.username}"

    class Meta:
        unique_together = ('client', 'date_time')

# ----------------------------------------

class Event(models.Model):
    id_event = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    creator = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='created_events', 
        limit_choices_to={'groups__name': 'ventas'}  # Limits to users in the "ventas" group.
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    # Many-to-many relationship with Cliente
    invited_clients = models.ManyToManyField(Cliente, related_name='events', blank=True)
