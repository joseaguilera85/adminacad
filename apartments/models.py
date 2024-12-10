from django.db import models


class Project(models.Model):
    TIPO_CHOICES = [
        ('Vivienda Vertical', 'Vivienda vertical'),
        ('Lotes', 'Lotes'),
        ('Casas', 'Casas'),
    ]

    name = models.CharField(max_length=40)
    location = models.CharField(max_length=40)
    start_date = models.DateField(null=True, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='disponible')
    description = models.CharField(max_length=700)
    image = models.ImageField(upload_to='media/projects/', null=True, blank=True)  # Add this line for image upload
    plano = models.ImageField(upload_to='media/apartments/plano/', null=True, blank=True)  # Add this line for image upload

    def __str__(self):
        return self.name

    #-----------------------------------


class Apartment(models.Model):
    STATUS_CHOICES = [
        ('disponible', 'Disponible'),
        ('apartado', 'Apartado'),
        ('vendido', 'Vendido'),
    ]

    project = models.ForeignKey(Project, related_name='apartments', on_delete=models.CASCADE)
    number = models.CharField(max_length=10)
    tipologia = models.CharField(max_length=10, default="A1")
    area = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='disponible')
    points = models.JSONField()  # Store the points of the polygon (e.g., [(x1, y1), (x2, y2), ...])
    image = models.ImageField(upload_to='media/apartments/', null=True, blank=True)  # Add this line for image upload

    def __str__(self):
        return f"Apartment {self.number} - Project: {self.project}"
