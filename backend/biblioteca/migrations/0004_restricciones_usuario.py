from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('biblioteca', '0003_proteger_historial_prestamos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='dni',
            field=models.CharField(max_length=8, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='telefono',
            field=models.CharField(max_length=12),
        ),
    ]
