# Navegación del Sistema

## Acceso

### Inicio de sesión

`/login/`

Permite autenticar al usuario del sistema.

### Panel principal

`/`

Requiere autenticación y muestra las estadísticas generales y accesos principales.

## Usuarios

- `/usuarios/` — listado y búsqueda
- `/usuarios/nuevo/` — registro
- `/usuarios/editar/<dni>/` — edición
- `/usuarios/eliminar/<dni>/` — confirmación de eliminación

## Libros

- `/libros/` — listado, búsqueda y filtros
- `/libros/nuevo/` — registro
- `/libros/editar/<id_libro>/` — edición
- `/libros/eliminar/<id_libro>/` — confirmación de eliminación

## Préstamos

- `/prestamos/` — listado, búsqueda y filtros
- `/prestamos/nuevo/` — registro de préstamo
- `/prestamos/devolver/<id_prestamo>/` — devolución

## Administración de Django

`/admin/`

Panel administrativo complementario de Django.
