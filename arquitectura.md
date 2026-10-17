# Arquitectura — Biblioteca Córdoba

**Actualización:** 16/10/2026. Documento descriptivo de la estructura del proyecto. La ejecución de pruebas y la configuración de producción deben verificarse en el entorno donde se despliegue.

## Capas

1. **Interfaz:** plantillas Django en `backend/biblioteca/templates/` y archivos estáticos en `backend/biblioteca/static/`.
2. **Rutas:** `backend/config/urls.py` monta las rutas globales; `backend/biblioteca/urls.py` define las rutas de la aplicación.
3. **Vistas y acceso:** `backend/biblioteca/views.py` procesa solicitudes y aplica controles de acceso. El bibliotecario usa una identidad propia y una sesión de aplicación; el lector utiliza autenticación Django y su perfil asociado.
4. **Formularios:** `backend/biblioteca/forms.py` valida datos recibidos. Los atributos HTML ayudan a la interfaz, pero no sustituyen la validación del servidor.
5. **Modelos:** `Usuario`, `Libro`, `Prestamo`, `PerfilBiblioteca`, `SolicitudPrestamo`, `MensajeSoporte` y `Bibliotecario`, además del modelo de usuario de Django.
6. **Persistencia:** SQLite se utiliza en desarrollo según la configuración local; para producción se puede configurar PostgreSQL mediante variables de entorno.
7. **Servicios opcionales:** correo SMTP para activación/recuperación y proveedor externo de IA para BiblioBot cuando se configura.

## Identidades y permisos

- **Lector:** cuenta de Django vinculada a una ficha `Usuario` mediante `PerfilBiblioteca`. El acceso a datos personales debe limitarse al lector autenticado.
- **Bibliotecario:** modelo independiente `Bibliotecario`; la autorización de sus vistas se realiza mediante la sesión propia. No se debe dibujar una FK en el ERD si no existe en los modelos.
- **Superusuario:** cuenta Django con permisos para `/admin/`.

## Regla de préstamo

Un libro con un préstamo activo debe permanecer en estado `Prestado`. El flujo de devolución debe cerrar el préstamo y registrar la fecha antes de volver a dejar el libro disponible, manteniendo la operación coherente.

## Archivos principales

- `backend/config/settings.py`: configuración de Django, base de datos y variables de entorno.
- `backend/config/urls.py` y `backend/biblioteca/urls.py`: rutas.
- `backend/biblioteca/views.py`: vistas y flujos.
- `backend/biblioteca/forms.py`: formularios y validación.
- `backend/biblioteca/models.py`: modelos y reglas de integridad.
- `backend/biblioteca/admin.py`: panel de administración de Django.
- `backend/biblioteca/migrations/`: migraciones versionadas, incluida la `0011` para los campos DNI y teléfono.
