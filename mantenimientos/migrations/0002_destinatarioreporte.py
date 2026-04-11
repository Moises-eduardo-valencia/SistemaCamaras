from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mantenimientos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DestinatarioReporte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empresa', models.CharField(max_length=100, verbose_name='Empresa')),
                ('email', models.EmailField(verbose_name='Correo electrónico')),
                ('activo', models.BooleanField(default=True, verbose_name='Activo')),
            ],
            options={
                'verbose_name': 'Destinatario de reporte',
                'verbose_name_plural': 'Destinatarios de reportes',
                'ordering': ['empresa', 'email'],
                'unique_together': {('empresa', 'email')},
            },
        ),
    ]
