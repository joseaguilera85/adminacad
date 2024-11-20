# analysis/forms.py

from django import forms
from .models import ProjectCost

class ProjectCostForm(forms.ModelForm):
    class Meta:
        model = ProjectCost
        fields = [
            'imprevistos_hard', 'iva_hard_cost',
            'pre_planeacion', 'tramites_permisos', 'legal_fiscal',
            'proyecto_ejecutivo', 'gerencia_de_obra', 'ingenierias_estudios',
            'fee_desarrollo', 'comercializacion', 'mercadotecnia',
            'imprevistos_soft', 'iva_soft_cost',
            'inflacion', 'tasa_interes', 'caja_inicial',
            'comision_contraventa', 'comision_contraescritura'
        ]

#-------------------------------

class ProjectTerrenoForm(forms.ModelForm):
    class Meta:
        model = ProjectCost
        fields = [
            'superficie_terreno', 'costo_terreno', 
            'costo_area_vendible_lotes',
            'cesion_municipal', 'costo_exterior_municipal',
            'vialidades_pavimentos','costo_vialidades_pavimentos',
            'jardines_amenidades_externas','costo_exterior_municipal',
            'areas_amenidades_lotes', 'areas_comunes_lotes', 'costo_amenidades_externas'
        ]

class ProjectFechasForm(forms.ModelForm):
    class Meta:
        model = ProjectCost
        fields = [
            'fecha_inicio_proyecto', 'mes_inicio_proyecto', 'fecha_fin_proyecto',
            'fecha_inicio_preventa',
            'fecha_inicio_construccion', 'fecha_fin_construccion',
            'fecha_inicio_preplaneacion', 'fecha_fin_preplaneacion',
            'fecha_inicio_mkt', 'fecha_fin_mkt',
            'fecha_inicio_tramites', 'fecha_fin_tramites',
            'fecha_inicio_legal_fiscal', 'fecha_fin_legal_fiscal',
            'fecha_inicio_proy_ejecutivo', 'fecha_fin_proy_ejecutivo',
        ]


class ProjectVentasForm(forms.ModelForm):
    class Meta:
        model = ProjectCost
        fields = [
            'numero_lotes', 'tamaño_promedio_lotes', 'absorcion_mensual_lotes', 'escrituracion_por_mes_lotes',
            'precio_por_m2', 'enganche_lotes','financiamiento_lotes','liquidacion_lotes','plazo_financiamiento_lotes',
            'incremento_precio_por_ud_vendidas_lotes','incremento_precio_lotes'
        ]