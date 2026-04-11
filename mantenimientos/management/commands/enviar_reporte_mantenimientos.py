from django.core.management.base import BaseCommand, CommandError

from mantenimientos.reports import enviar_reporte_mantenimientos


class Command(BaseCommand):
    help = 'Envía el reporte mensual de mantenimientos realizados por empresa'

    def add_arguments(self, parser):
        parser.add_argument('--empresa', type=str, default=None)
        parser.add_argument('--mes', type=str, default=None,
                            help='Formato YYYY-MM (por defecto: mes anterior)')

    def handle(self, *args, **options):
        año, mes = None, None
        if options.get('mes'):
            try:
                año, mes = map(int, options['mes'].split('-'))
            except ValueError:
                raise CommandError('--mes debe tener el formato YYYY-MM')

        enviados, errores = enviar_reporte_mantenimientos(options.get('empresa'), año, mes)
        self.stdout.write(self.style.SUCCESS(f'Enviados: {enviados}'))
        if errores:
            self.stdout.write(self.style.ERROR(f'Errores: {errores}'))
