# models.py
from django.db import models
from apartments.models import Project

#---------------------------

# Choice fields for categoria and subcategoria
CATEGORIA_CHOICES = [
    ('terreno', 'Terreno'),
    ('soft_cost', 'Soft Cost'),
    ('hard_cost', 'Hard Cost'),
]

SUBCATEGORIA_CHOICES = [
    # Soft Cost Categories
    ('pre_planeacion', 'Pre-planeación'),
    ('honorarios_arquitectura', 'Honorarios de Arquitectura e Ingeniería'),
    ('honorarios_legales', 'Honorarios Legales'),
    ('permisos_licencias', 'Permisos y Licencias'),
    ('proyecto_ejecutivo', 'Proyecto ejecutivo'),
    ('gerencia_obra', 'Gerencia de obra'),
    ('gestion_proyecto', 'Gestión del Proyecto'),
    ('gastos_financieros', 'Gastos Financieros'),
    ('gastos_publicidad', 'Gastos de Publicidad y Marketing'),
    ('gastos_comercializacion', 'Gastos de comercialización'),
    ('otros_soft_cost', 'Otros (Soft Cost)'),

    # Hard Cost Categories
    ('demolicion_preparacion', 'Demolición y Preparación del Terreno'),
    ('cimentacion_estructura', 'Cimentación y Estructura'),
    ('costos_materiales', 'Costos de Materiales de Construcción'),
    ('electricidad_fontaneria', 'Electricidad y Fontanería'),
    ('suelos_acabados', 'Suelos y Acabados'),
    ('mobiliario_decoracion', 'Mobiliario y Decoración Fijos'),
    ('paisajismo_areas_verdes', 'Paisajismo y Áreas Verdes'),
    ('mano_obra', 'Mano de Obra'),
    ('otros_hard_cost', 'Otros (Hard Cost)'),

    # Terreno Category
    ('terreno', 'Terreno'),
]

class Vendor(models.Model):
    empresa = models.CharField(max_length=50)
    persona = models.CharField(max_length=50)
    fiscal_id = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    telephone = models.CharField(max_length=15)
    address = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    CP = models.CharField(max_length=50)

    def __str__(self):
       return f"{self.empresa} {self.persona}"

#---------------------------

STATUS_CHOICES = [
    ('pendiente', 'Pendiente'),
    ('enviada', 'Enviada'),
    ('recibida', 'Recibida'),
    ('pagada', 'Pagada'),
]

class PurchaseOrder(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='purchaseorder')
    empresa = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pendiente')  # Default set to 'Pendiente'

    @property
    def total(self):
        """Calculates the total of the purchase order by summing the total of all items."""
        return sum(item.total_amount for item in self.items.all())

    def __str__(self):
        return f"{self.id}"

class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    categoria = models.CharField(max_length=30, choices=CATEGORIA_CHOICES)
    subcategoria = models.CharField(max_length=30, choices=SUBCATEGORIA_CHOICES)
    item_name = models.CharField(max_length=255)
    
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_amount(self):
        """Calculates total amount of the item (quantity * price)."""
        return self.quantity * self.price

    def __str__(self):
        return f"{self.item_name} ({self.quantity} x {self.price})"

class Egreso(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='egresos')
    categoria = models.CharField(max_length=30, choices=CATEGORIA_CHOICES)
    subcategoria = models.CharField(max_length=30, choices=SUBCATEGORIA_CHOICES)
    empresa = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.project} - {self.categoria} - {self.subcategoria}"
