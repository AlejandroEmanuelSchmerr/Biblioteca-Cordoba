from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [('biblioteca', '0007_portal_lector_solicitudes_soporte')]
    operations = [migrations.CreateModel(name='Bibliotecario', fields=[
        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        ('username', models.CharField(max_length=60, unique=True)),
        ('nombre', models.CharField(max_length=80)),
        ('apellido', models.CharField(max_length=80)),
        ('email', models.EmailField(max_length=254, unique=True)),
        ('password', models.CharField(max_length=128)),
        ('activo', models.BooleanField(default=True)),
        ('creado', models.DateTimeField(auto_now_add=True)),
    ])]
