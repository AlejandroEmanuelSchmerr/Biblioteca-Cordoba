from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [('biblioteca', '0009_limite_email_50')]
    operations = [
        migrations.AddField(model_name='prestamo', name='bibliotecario_registra', field=models.ForeignKey(blank=True, help_text='Personal que registró el préstamo; vacío en registros históricos o automáticos.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prestamos_registrados', to='biblioteca.bibliotecario')),
        migrations.AddField(model_name='solicitudprestamo', name='bibliotecario_responsable', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='solicitudes_atendidas', to='biblioteca.bibliotecario')),
        migrations.AddField(model_name='mensajesoporte', name='bibliotecario_responde', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mensajes_respondidos', to='biblioteca.bibliotecario')),
    ]
