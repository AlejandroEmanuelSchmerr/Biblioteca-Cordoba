# Límite de correo electrónico — 14/10/2026

Se establece un máximo de **50 caracteres** para los correos de lectores y bibliotecarios. La regla se aplica en el modelo y en los formularios, y el atributo HTML `maxlength` evita escribir más de 50 caracteres desde el navegador. La validación del servidor sigue siendo la autoridad.

Se añadió la migración `0009_limite_email_50.py`. En una copia de seguridad de la base de datos, ejecutar desde `backend`: `python manage.py migrate`. Antes de aplicar el cambio en una base existente, revisar si ya hay correos de más de 50 caracteres; esos registros deben corregirse antes de migrar para no perder datos.

Nota: un límite de 50 caracteres es una decisión de este proyecto; algunos correos válidos pueden ser más largos.
