from django.db import migrations, models
import django.db.models.deletion


def guardar_datos_historicos(apps, schema_editor):
    Prestamo = apps.get_model('biblioteca', 'Prestamo')
    for prestamo in Prestamo.objects.select_related('dni', 'id_libro').all().iterator():
        cambios = []
        if prestamo.dni_id:
            prestamo.usuario_nombre_historico = f'{prestamo.dni.nombre} {prestamo.dni.apellido}'
            prestamo.usuario_dni_historico = prestamo.dni.dni
            cambios.extend(['usuario_nombre_historico', 'usuario_dni_historico'])
        if prestamo.id_libro_id:
            prestamo.libro_titulo_historico = prestamo.id_libro.titulo
            prestamo.libro_autor_historico = prestamo.id_libro.autor
            cambios.extend(['libro_titulo_historico', 'libro_autor_historico'])
        if cambios:
            prestamo.save(update_fields=cambios)


class Migration(migrations.Migration):
    dependencies = [('biblioteca', '0004_restricciones_usuario')]

    operations = [
        migrations.AddField(
            model_name='prestamo', name='usuario_nombre_historico',
            field=models.CharField(blank=True, default='', max_length=110),
        ),
        migrations.AddField(
            model_name='prestamo', name='usuario_dni_historico',
            field=models.CharField(blank=True, default='', max_length=8),
        ),
        migrations.AddField(
            model_name='prestamo', name='libro_titulo_historico',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
        migrations.AddField(
            model_name='prestamo', name='libro_autor_historico',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.RunPython(guardar_datos_historicos, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='prestamo', name='dni',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prestamos', to='biblioteca.usuario'),
        ),
        migrations.AlterField(
            model_name='prestamo', name='id_libro',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prestamos', to='biblioteca.libro'),
        ),
    ]
