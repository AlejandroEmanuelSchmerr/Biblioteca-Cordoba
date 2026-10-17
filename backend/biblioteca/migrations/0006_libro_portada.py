# Generated for Biblioteca Córdoba: book cover image support.
from django.db import migrations, models
import django.core.validators

class Migration(migrations.Migration):
    dependencies = [('biblioteca', '0005_historial_eliminaciones_y_comprobantes')]
    operations = [migrations.AddField(
        model_name='libro', name='portada',
        field=models.ImageField(blank=True, help_text='Imagen JPG, PNG o WEBP. Máximo 5 MB (validado también en el formulario).', null=True, upload_to='portadas_libros/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])]),
    )]
