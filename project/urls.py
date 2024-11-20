
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', include('menu.urls')),
    path("admin/", admin.site.urls),

    path('menu/', include('menu.urls')),
    path('appname/', include('appname.urls')),
    path('pagos/', include('pagos.urls')), 
    path('apartments/', include('apartments.urls')),
    path('clientes/', include('clientes.urls')),
    path('analysis/', include('analysis.urls')),
    path('egresos/', include('egresos.urls')),
     path('bancos/', include('bancos.urls')),  # Include bancos app URL

]


# This serves media files during development (when DEBUG is True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)