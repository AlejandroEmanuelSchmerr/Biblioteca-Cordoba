# Diagramas de Biblioteca Córdoba — 14/10/2026

## Archivos editables
1. `diagramas/01_Arquitectura_Roles.drawio`: roles, rutas, vistas, formularios, modelos, plantillas, servicios y base de datos.
2. `diagramas/02_Flujo_Completo_Proyecto.drawio`: entrada, roles, portal lector, panel bibliotecario, administración Django, préstamos, devoluciones y soporte.
3. `diagramas/03_Entidad_Relacion_Modelos_Reales.drawio`: entidades y relaciones ORM inferidas de `biblioteca/models.py`.
4. `diagramas/04_Diagrama_Base_Datos.drawio`: representación física aproximada de tablas de la app y tablas administradas por Django.

## Diferencia ER vs base de datos
El ER prioriza entidades y cardinalidades. El diagrama de base de datos prioriza tablas, columnas, tipos aproximados, claves e infraestructura Django. Las tablas internas de Django varían según versión y migraciones aplicadas.

## Relaciones representadas
- `PerfilBiblioteca.cuenta` es OneToOne con `AUTH_USER_MODEL`; `PerfilBiblioteca.usuario` es OneToOne con `Usuario`.
- `Prestamo.dni` y `Prestamo.id_libro` permiten NULL y usan SET_NULL; los campos históricos preservan datos descriptivos.
- `SolicitudPrestamo.usuario` y `SolicitudPrestamo.libro` usan PROTECT.
- `MensajeSoporte.usuario_cuenta` apunta al usuario autenticado de Django.
- `Bibliotecario` es una tabla de credenciales propia; no es una FK a `auth_user`.

Abrir archivos `.drawio` desde diagrams.net. Los `.mmd` son fuentes de texto alternativas. Revisar siempre las relaciones si los modelos cambian.
