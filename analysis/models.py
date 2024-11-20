from django.db import models
from apartments.models import Project
from datetime import datetime
from dateutil.relativedelta import relativedelta  # This is useful for month calculations


class ProjectCost(models.Model):
    # Cost Details with Default Values
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='costs')
    imprevistos_hard = models.FloatField(default=5.0)  # Default 5%
    iva_hard_cost = models.FloatField(default=16.0)    # Default 16%

    # Soft Costs and Taxes with Default Values
    pre_planeacion = models.FloatField(default=2.0)    # Default 2%
    tramites_permisos = models.FloatField(default=3.0) # Default 3%
    legal_fiscal = models.FloatField(default=2.5)      # Default 2.5%
    proyecto_ejecutivo = models.FloatField(default=6.0)# Default 6%
    gerencia_de_obra = models.FloatField(default=7.0)  # Default 7%
    ingenierias_estudios = models.FloatField(default=1.5) # Default 1.5%
    fee_desarrollo = models.FloatField(default=8.0)    # Default 8%
    comercializacion = models.FloatField(default=3.0)  # Default 3%
    mercadotecnia = models.FloatField(default=2.5)     # Default 2.5%
    imprevistos_soft = models.FloatField(default=5.0)  # Default 5%
    iva_soft_cost = models.FloatField(default=16.0)    # Default 16%

    # Additional Financial Details with Default Values
    inflacion = models.FloatField(default=4.0)         # Default 4%
    tasa_interes = models.FloatField(default=7.0)      # Default 7%
    caja_inicial = models.FloatField(default=10000.0)  # Default $10,000

    # Commissions with Default Values
    comision_contraventa = models.FloatField(default=1.0)  # Default 1%
    comision_contraescritura = models.FloatField(default=1.0)  # Default 1%

    # Project Dates
    fecha_inicio_proyecto = models.DateField(default=datetime.today)
    mes_inicio_proyecto = models.IntegerField(default=1)
    
    def default_fecha_fin_proyecto():
        return datetime.today() + relativedelta(months=48)

    fecha_fin_proyecto = models.DateField(default=default_fecha_fin_proyecto)
    
    def default_fecha_inicio_preventa():
        return datetime.today() + relativedelta(months=18)

    fecha_inicio_preventa = models.DateField(default=default_fecha_inicio_preventa)

    # Construcción Dates
    fecha_inicio_construccion = models.DateField(default=datetime.today)
    fecha_fin_construccion = models.DateField(default=datetime.today)

    # Pre-planeación Dates
    fecha_inicio_preplaneacion = models.DateField(default=datetime.today)
    fecha_fin_preplaneacion = models.DateField(default=datetime.today)

    # Marketing Dates
    fecha_inicio_mkt = models.DateField(default=datetime.today)
    fecha_fin_mkt = models.DateField(default=datetime.today)

    # Permits (Trámites) Dates
    fecha_inicio_tramites = models.DateField(default=datetime.today)
    fecha_fin_tramites = models.DateField(default=datetime.today)

    # Legal and Fiscal Dates
    fecha_inicio_legal_fiscal = models.DateField(default=datetime.today)
    fecha_fin_legal_fiscal = models.DateField(default=datetime.today)

    # Executive Project (Proyecto Ejecutivo) Dates
    fecha_inicio_proy_ejecutivo = models.DateField(default=datetime.today)
    fecha_fin_proy_ejecutivo = models.DateField(default=datetime.today)

    # Land Details
    superficie_terreno = models.FloatField(null=True, blank=True)
    costo_terreno = models.FloatField(null=True, blank=True)
    
    cesion_municipal = models.FloatField(null=True, blank=True)
    vialidades_pavimentos = models.FloatField(null=True, blank=True)
    jardines_amenidades_externas = models.FloatField(null=True, blank=True)
    areas_amenidades_lotes = models.FloatField(null=True, blank=True)
    areas_comunes_lotes = models.FloatField(null=True, blank=True)

    # Lot Variables
    numero_lotes = models.IntegerField(null=True, blank=True)
    tamaño_promedio_lotes = models.FloatField(null=True, blank=True)
    absorcion_mensual_lotes = models.IntegerField(null=True, blank=True)
    escrituracion_por_mes_lotes = models.IntegerField(null=True, blank=True)

    # Sales and Financing Details
    precio_por_m2 = models.FloatField(null=True, blank=True)
    enganche_lotes = models.FloatField(null=True, blank=True)
    financiamiento_lotes = models.FloatField(null=True, blank=True)
    liquidacion_lotes = models.FloatField(null=True, blank=True)
    plazo_financiamiento_lotes = models.FloatField(null=True, blank=True)
    incremento_precio_por_ud_vendidas_lotes = models.FloatField(null=True, blank=True)
    incremento_precio_lotes = models.FloatField(null=True, blank=True)

    # Cost Details
    costo_area_vendible_lotes = models.FloatField(null=True, blank=True)
    costo_amenidades_externas = models.FloatField(null=True, blank=True)
    costo_vialidades_pavimentos = models.FloatField(null=True, blank=True)
    costo_exterior_municipal = models.FloatField(null=True, blank=True)


 