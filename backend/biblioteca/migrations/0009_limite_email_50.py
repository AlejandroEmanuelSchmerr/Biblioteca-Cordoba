from django.db import migrations, models
import biblioteca.models


class Migration(migrations.Migration):
    dependencies = [("biblioteca", "0008_bibliotecario_independiente")]

    operations = [
        migrations.AlterField(
            model_name="usuario",
            name="email",
            field=models.EmailField(max_length=50, validators=[biblioteca.models.validar_email_biblioteca]),
        ),
        migrations.AlterField(
            model_name="bibliotecario",
            name="email",
            field=models.EmailField(max_length=50, unique=True),
        ),
    ]
