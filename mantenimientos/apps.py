import sys

from django.apps import AppConfig


class MantenimientosConfig(AppConfig):
    name = 'mantenimientos'

    def ready(self):
        # No arrancar el scheduler en comandos de manage.py (migrate, test, etc.)
        # Solo arrancarlo cuando corre el servidor real
        if 'runserver' in sys.argv or 'gunicorn' in sys.argv[0]:
            from mantenimientos.scheduler import iniciar_scheduler
            iniciar_scheduler()
