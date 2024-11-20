from django.db import models
from adminacad.models import Student

class BankAccountMovement(models.Model):
    """
    Model representing a bank account movement.
    """

    TRANSACTION_TYPES = (
        ('A', 'Cargos Colegiatura'),
        ('B', 'Cargos Seguro'),
        ('C', 'Cargos Cuotas'),
        ('D', 'Pagos Colegiatura'),
        ('E', 'Pagos Seguro'),
        ('F', 'Pagos Cuotas'),
    )

    transaction_date = models.DateField(auto_now_add=False)
    transaction_type = models.CharField(max_length=1, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)        

    def __str__(self):
        date_str = self.transaction_date.strftime('%d/%b/%y')
        return f"{date_str} - {self.get_transaction_type_display()} - ${self.amount} - {self.student.identificacion}"

