# Roles y aislamiento de cuentas — Biblioteca Córdoba

## Identidades independientes
- **Administrador principal:** cuenta de Django `auth.User` con `is_superuser=True`; administra desde `/admin/`.
- **Bibliotecario:** registro propio en la tabla `biblioteca_bibliotecario`, con usuario, contraseña hasheada, estado activo y sesión independiente en `bibliotecario_id`. Se crea desde Django Admin; no necesita una cuenta lectora ni una ficha `Usuario`. Acceso por `/bibliotecario/login/`.
- **Lector:** cuenta de autenticación Django no privilegiada, vinculada a una ficha de biblioteca mediante `PerfilBiblioteca`; acceso por `/login/` y registro por `/registro/`.
- **Ficha de usuario:** tabla `biblioteca_usuario`, contiene datos de la persona y no credenciales.

## Aislamiento de navegación
Las vistas de gestión interna verifican la sesión independiente de bibliotecario. El portal lector verifica la cuenta de lector y su perfil asociado. `/admin/` es exclusivo para superusuarios. En la pantalla de acceso de bibliotecario no se muestra un enlace al acceso lector; en las pantallas de lector no se muestra el acceso de personal.

## Inicio de sesión del bibliotecario
El usuario y contraseña se definen cuando el administrador crea el registro en Django Admin → Bibliotecarios. No hay credenciales predeterminadas. Para entrar se utiliza el `username` creado y la contraseña asignada.

## Pruebas
Las pruebas de vistas internas deben crear un objeto `Bibliotecario` y guardar su PK en `client.session['bibliotecario_id']`. No se debe simular al personal con `auth.User.is_staff`, ya que son identidades distintas. Ejecutar `python manage.py test` tras cada cambio.

## Nota de seguridad
La separación de identidades no sustituye la revisión de permisos de cada vista, la protección CSRF, HTTPS, secretos de entorno ni la verificación de acceso a cada objeto. Antes de desplegar en producción, ejecutar `python manage.py check --deploy` y revisar todos los tests.
