from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('biblioteca', '0006_libro_portada'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PerfilBiblioteca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('cuenta', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil_biblioteca', to=settings.AUTH_USER_MODEL)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil_cuenta', to='biblioteca.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='SolicitudPrestamo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('Pendiente', 'Pendiente'), ('Aprobada', 'Aprobada'), ('Rechazada', 'Rechazada')], default='Pendiente', max_length=12)),
                ('creada', models.DateTimeField(auto_now_add=True)),
                ('respondida', models.DateTimeField(blank=True, null=True)),
                ('nota_bibliotecario', models.CharField(blank=True, default='', max_length=300)),
                ('libro', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='solicitudes_prestamo', to='biblioteca.libro')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='solicitudes_prestamo', to='biblioteca.usuario')),
            ],
            options={'ordering': ['-creada']},
        ),
        migrations.CreateModel(
            name='MensajeSoporte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mensaje', models.CharField(max_length=1500)),
                ('respuesta', models.CharField(blank=True, default='', max_length=3000)),
                ('solicita_persona', models.BooleanField(default=False)),
                ('atendido', models.BooleanField(default=False)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('respondido', models.DateTimeField(blank=True, null=True)),
                ('usuario_cuenta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mensajes_biblioteca', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['creado']},
        ),
    ]
