from django.contrib import admin
from django.utils.html import format_html
from .models import Project, Apartment

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'start_date', 'image_preview','plano_preview')
    search_fields = ('name', 'location')
    list_filter = ('start_date',)
    readonly_fields = ('image_preview','plano_preview')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 100px; width: auto;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = "Image Preview"

    def plano_preview(self, obj):
        if obj.plano:
            return format_html('<img src="{}" style="height: 100px; width: auto;" />', obj.plano.url)
        return "No Image"
    plano_preview.short_description = "Plano Preview"


class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('number', 'project', 'tipologia', 'area', 'status', 'image_preview')
    search_fields = ('number', 'project__name')
    list_filter = ('status', 'project')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 100px; width: auto;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = "Image Preview"


admin.site.register(Project, ProjectAdmin)
admin.site.register(Apartment, ApartmentAdmin)