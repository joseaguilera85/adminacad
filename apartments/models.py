from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    start_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='media/apartments/', null=True, blank=True)  # Add this line for image upload

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

    def __str__(self):
        return f"Apartment {self.number} - Project: {self.project}"
