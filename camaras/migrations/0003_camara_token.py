import uuid

from django.db import migrations, models


def generar_tokens(apps, schema_editor):
    Camara = apps.get_model('camaras', 'Camara')
    for camara in Camara.objects.all():
        camara.token = uuid.uuid4()
        camara.save(update_fields=['token'])


class Migration(migrations.Migration):

    dependencies = [
        ('camaras', '0002_camara_created_at_camara_updated_at'),
    ]

    operations = [
        # Paso 1: agregar la columna nullable (sin unique todavía)
        migrations.AddField(
            model_name='camara',
            name='token',
            field=models.UUIDField(null=True, editable=False),
        ),
        # Paso 2: poblar con UUIDs únicos
        migrations.RunPython(generar_tokens, migrations.RunPython.noop),
        # Paso 3: hacer el campo NOT NULL + UNIQUE
        migrations.AlterField(
            model_name='camara',
            name='token',
            field=models.UUIDField(default=uuid.uuid4, unique=True, editable=False),
        ),
    ]
