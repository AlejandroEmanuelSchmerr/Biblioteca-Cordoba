# Seguridad y despliegue

## Antes de publicar

- Configurar `DEBUG=False` y `ALLOWED_HOSTS` para el dominio de despliegue.
- Mantener `SECRET_KEY`, credenciales SMTP, claves de API y contraseñas fuera del repositorio, usando variables de entorno o el gestor de secretos del hosting.
- Activar HTTPS y revisar cookies seguras, CSRF, sesiones y cabeceras recomendadas por Django.
- Configurar una base de datos de producción (por ejemplo, PostgreSQL), ejecutar migraciones y preparar copias de seguridad.
- Ejecutar `python manage.py check --deploy` con la configuración real de producción.
- Configurar archivos estáticos y archivos multimedia/portadas; no asumir que `runserver` sirve como configuración de producción.
- Crear cuentas de prueba y verificar que lector, bibliotecario y superusuario tengan permisos distintos.
- Probar registro/activación por correo, recuperación de contraseña, préstamos, devoluciones, soporte y generación de PDF.
- No subir una base de datos con información personal real a un repositorio público.

## Publicación general

1. Subir el código limpio a GitHub, con `.gitignore` correcto.
2. Crear una aplicación en un hosting compatible con Django y una base de datos.
3. Configurar variables de entorno, dominio y correo SMTP.
4. Instalar dependencias, ejecutar migraciones y recolectar estáticos (`python manage.py collectstatic`).
5. Ejecutar `python manage.py check --deploy` y las pruebas.
6. Verificar la web publicada con cuentas de prueba y revisar logs.

## Límites

La lista es una guía de preparación, no una certificación de seguridad. No se debe afirmar que el sistema es invulnerable o que cumple automáticamente con toda normativa de privacidad. Revisar las versiones de Django y dependencias y corregir advertencias antes de producción.


