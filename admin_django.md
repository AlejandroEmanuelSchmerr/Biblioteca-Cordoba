# Administración del Sistema

## Panel de Administración

Biblioteca Córdoba utiliza el panel de administración integrado de Django como herramienta complementaria de gestión.

## Modelos registrados

- Usuario
- Libro
- Préstamo

## Personalización

Se configuró `ModelAdmin` para mostrar información relevante mediante `list_display`, además de búsquedas y filtros donde corresponde.

## Seguridad

El panel `/admin/` utiliza el sistema de autenticación y permisos de Django. No debe confundirse con la interfaz principal del bibliotecario.
