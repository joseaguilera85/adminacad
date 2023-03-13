from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

class Salones(models.Model):
    salon = models.CharField(max_length=50)
    grado = models.IntegerField()
    profesor = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.salon} - {self.profesor}"
    
    def get_grado_str(self):
        return str(self.grado)

class Student(models.Model):
    nombre_est = models.CharField(max_length=100)
    apellido_est = models.CharField(max_length=100)
    salon = models.ForeignKey(Salones, on_delete=models.CASCADE)
    identificacion = models.IntegerField(unique=True, validators=[
        MaxValueValidator(2000, message='Identificacion must be less than or equal to 2000.'),
        MinValueValidator(1000, message='Identificacion must be greater than or equal to 1000.'),
    ])
    grado = models.ForeignKey(Salones, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return self.nombre_est

class Materias(models.Model):
    nombre_materia = models.CharField(max_length=100)
    clave_materia = models.CharField(max_length=100)
    grado = models.ForeignKey(Salones, on_delete=models.CASCADE)

    def __str__(self):
        return self.clave_materia

class Calificacion(models.Model):
    calif = models.IntegerField(default=0)
    calif_1B = models.IntegerField(default=0)
    calif_2B = models.IntegerField(default=0)
    calif_3B = models.IntegerField(default=0)
    calif_4B = models.IntegerField(default=0)
    calif_5B = models.IntegerField(default=0)
    identificacion = models.ForeignKey(Student, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materias, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('identificacion', 'materia')

@receiver(post_save, sender=Student)
def create_grade(sender, instance, created, **kwargs):
    if created:
        materias = Materias.objects.filter(grado=instance.salon.grado)
        for materia in materias:
            Calificacion.objects.create(identificacion=instance, materia=materia)


