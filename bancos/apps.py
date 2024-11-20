# bancos/apps.py
from django.apps import AppConfig

class BancosConfig(AppConfig):
    name = 'bancos'

    def ready(self):
        import bancos.signals  # This will connect the signal
