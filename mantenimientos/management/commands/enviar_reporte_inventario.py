from django.core.management.base import BaseCommand

from mantenimientos.reports import enviar_reporte_inventario


class Command(BaseCommand):
    help = 'Envía el reporte mensual de inventario de cámaras por empresa'

    def add_arguments(self, parser):
        parser.add_argument('--empresa', type=str, default=None,
                            help='Enviar solo para esta empresa')

    def handle(self, *args, **options):
        enviados, errores = enviar_reporte_inventario(options.get('empresa'))
        self.stdout.write(self.style.SUCCESS(f'Enviados: {enviados}'))
        if errores:
            self.stdout.write(self.style.ERROR(f'Errores: {errores}'))
