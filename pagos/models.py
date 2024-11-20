from django.db import models
from apartments.models import Apartment, Project  # Ensure correct import
from clientes.models import Cliente


class ListaCliente:
    def __init__(self, cliente):
        self.cliente = cliente

    def get_full_name(self):
        return f"{self.cliente.nombre} {self.cliente.apellido}"

    def get_contact_info(self):
        return {
            "celular": self.cliente.celular,
            "mail": self.cliente.mail,
        }

    def get_client_status(self):
        return self.cliente.estatus
 
#--------------------------------

class PaymentPlan(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='payment_plans')
    status = models.ForeignKey(Apartment, on_delete=models.CASCADE, default="1")
    
    month = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=20)  # e.g., 'Enganche', 'Mensualidad', 'Pago final'

    def __str__(self):
        return f"Payment Plan for Apartment {self.apartment.number} - Month {self.month}"

#--------------------------------

class PaymentRecord(models.Model):
    cliente = models.CharField(max_length=255)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='payment_records')
    porcentaje_descuento = models.DecimalField(max_digits=5, decimal_places=2)
    porcentaje_enganche = models.DecimalField(max_digits=5, decimal_places=2)
    porcentaje_mensualidades = models.DecimalField(max_digits=5, decimal_places=2)
    num_mensualidades = models.IntegerField()
    mes_inicio = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='payment_records', null=True, blank=True)
    payment_schedule = models.JSONField(default=dict)

    def set_cliente(self, cliente):
        self.cliente = cliente
        self.save()

#--------------------------------

class PriceList(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='price_lists', null=True, blank=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='price_lists')
    list_number_0 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    list_number_1 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    list_number_2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    list_number_3 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    list_number_4 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    list_number_5 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    current_list_price_index = models.IntegerField(default=0, null=True, blank=True)


    @property
    def tipologia(self):
        return self.apartment.tipologia  # Access the tipologia from the related Apartment
    
    @property
    def current_list_price(self):
        # Return the current list price based on the index
        index = self.current_list_price_index
        if index is not None:
            if index == 0:
                return self.list_number_0
            elif index == 1:
                return self.list_number_1
            elif index == 2:
                return self.list_number_2
            elif index == 3:
                return self.list_number_3
            elif index == 4:
                return self.list_number_4
            elif index == 5:
                return self.list_number_5
        return None

    def __str__(self):
        return f"Price List for Apartment {self.apartment.number}"



# -------------------------------

class PaymentTransaction(models.Model):
    payment_record = models.ForeignKey(PaymentRecord, on_delete=models.CASCADE, related_name='transactions')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()

    def __str__(self):
        return f"Payment of {self.amount_paid} for {self.payment_record.cliente} on {self.payment_date}"

    def get_pending_balance(self):
        total_due = sum(payment['pago'] for payment in self.payment_schedule)
        total_paid = sum(transaction.amount_paid for transaction in self.transactions.all())
        return total_due - total_paid

# -------------------------------
from decimal import Decimal

class AccountStatement(models.Model):
    # Campos de AccountStatement
    payment_record = models.OneToOneField(PaymentRecord, on_delete=models.CASCADE, related_name='account_statement')
    total_due = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance_due = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calculate_totals(self):
        # Sumar el total de pagos realizados
        self.total_paid = sum(transaction.amount_paid for transaction in self.payment_record.transactions.all())
        
        self.total_due = Decimal(self.total_due)
        self.total_paid = Decimal(self.total_paid)

        # Calcular el balance como total adeudado menos el total pagado
        self.balance_due = self.total_due - self.total_paid
        self.save()