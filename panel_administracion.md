# Panel de Administración

## Objetivo

Documentar el panel de administración de Django utilizado para administrar los modelos del sistema.

## Modelos registrados

- Usuario
- Libro
- Préstamo

## Funciones

El panel permite:

- Crear registros
- Consultar registros
- Modificar registros
- Eliminar registros
- Buscar información
- Filtrar determinados registros

La personalización se encuentra en `backend/biblioteca/admin.py` mediante `ModelAdmin`.

## Acceso

Ruta:

`/admin/`

El acceso requiere una cuenta con permisos de administración de Django.

## Alcance

El panel de administración complementa la interfaz principal de Biblioteca Córdoba. Las operaciones habituales del bibliotecario se realizan desde la interfaz propia del sistema.
