import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("biblioteca", "0002_alter_libro_estado_alter_prestamo_estado"),
    ]

    operations = [
        migrations.AlterField(
            model_name="prestamo",
            name="dni",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="prestamos",
                to="biblioteca.usuario",
            ),
        ),
        migrations.AlterField(
            model_name="prestamo",
            name="id_libro",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="prestamos",
                to="biblioteca.libro",
            ),
        ),
    ]
