import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

logger = logging.getLogger(__name__)


def job_reporte_inventario():
    """Job: envía el reporte de inventario el día 1 de cada mes a las 8:00 AM."""
    from mantenimientos.reports import enviar_reporte_inventario
    logger.info('Ejecutando job: reporte de inventario')
    enviados, errores = enviar_reporte_inventario()
    logger.info('Reporte inventario — enviados: %d, errores: %d', enviados, errores)


def job_reporte_mantenimientos():
    """Job: envía el reporte del mes anterior el día 1 de cada mes a las 8:30 AM."""
    from mantenimientos.reports import enviar_reporte_mantenimientos
    logger.info('Ejecutando job: reporte de mantenimientos')
    enviados, errores = enviar_reporte_mantenimientos()
    logger.info('Reporte mantenimientos — enviados: %d, errores: %d', enviados, errores)


def limpiar_ejecuciones_antiguas():
    """Elimina registros de ejecuciones con más de 7 días para no acumular basura."""
    DjangoJobExecution.objects.delete_old_job_executions(7)


def iniciar_scheduler():
    timezone = getattr(settings, 'TIME_ZONE', 'America/Mexico_City')

    scheduler = BackgroundScheduler(timezone=timezone)
    scheduler.add_jobstore(DjangoJobStore(), 'default')

    # Reporte de inventario — día 1 de cada mes a las 8:00
    scheduler.add_job(
        job_reporte_inventario,
        trigger=CronTrigger(day=1, hour=8, minute=0),
        id='reporte_inventario_mensual',
        name='Reporte mensual de inventario',
        jobstore='default',
        replace_existing=True,
    )

    # Reporte de mantenimientos — día 1 de cada mes a las 8:30
    scheduler.add_job(
        job_reporte_mantenimientos,
        trigger=CronTrigger(day=1, hour=8, minute=30),
        id='reporte_mantenimientos_mensual',
        name='Reporte mensual de mantenimientos',
        jobstore='default',
        replace_existing=True,
    )

    # Limpieza de ejecuciones antiguas — todos los lunes a las 3:00 AM
    scheduler.add_job(
        limpiar_ejecuciones_antiguas,
        trigger=CronTrigger(day_of_week='mon', hour=3, minute=0),
        id='limpiar_ejecuciones',
        name='Limpieza de ejecuciones antiguas',
        jobstore='default',
        replace_existing=True,
    )

    scheduler.start()
    logger.info('Scheduler iniciado. Jobs registrados: %s',
                [j.id for j in scheduler.get_jobs()])
    return scheduler
