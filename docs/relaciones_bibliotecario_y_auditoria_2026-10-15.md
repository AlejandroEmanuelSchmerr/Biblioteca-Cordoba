# Relaciones de Bibliotecario y auditoría — 15/10/2026

La identidad `Bibliotecario` continúa separada de `AUTH_USER`, porque el proyecto utiliza una sesión de personal propia (`bibliotecario_id`). Para que no quede aislada en el modelo relacional y para guardar quién realizó operaciones, se agregan claves foráneas opcionales con `SET_NULL`: `Prestamo.bibliotecario_registra`, `SolicitudPrestamo.bibliotecario_responsable` y `MensajeSoporte.bibliotecario_responde`.

Estas referencias son opcionales para conservar compatibilidad con datos históricos. No se crea una relación artificial de Bibliotecario con cada libro: el libro no pertenece a un solo empleado. La relación de auditoría se registra sobre la operación realizada.

Migración añadida: `0010_relaciones_bibliotecario_auditoria.py`. Aplicar con `python manage.py migrate` después de realizar copia de seguridad.
