# Modelo de datos

Este documento se contrasta con `backend/biblioteca/models.py`. Si los modelos cambian, actualizar también `diagramas/Diagrama_Entidad_Relacion.drawio` y `diagramas/modelo_datos_actualizado_2026-10-13.mmd`.

## Entidades

- **Usuario** (`dni` PK): nombre, apellido, teléfono y email. Representa la ficha bibliotecaria, no la cuenta de autenticación.
- **Libro** (`id_libro` PK): título, autor, editorial, año, categoría, portada opcional y estado (`Disponible`, `Prestado`, `Reservado`).
- **Prestamo** (`id_prestamo` PK): referencias opcionales a `Usuario` y `Libro`, datos históricos de nombre/DNI/título/autor, fecha de préstamo, fecha de devolución y estado (`Activo`, `Devuelto`). Las copias históricas permiten conservar comprobantes aunque se elimine una ficha relacionada.
- **PerfilBiblioteca**: relación uno a uno entre la cuenta de Django y un `Usuario`.
- **SolicitudPrestamo**: solicitud de un lector para un libro, estado (`Pendiente`, `Aprobada`, `Rechazada`), fechas y nota del bibliotecario. Las relaciones a usuario y libro usan `PROTECT`.
- **MensajeSoporte**: cuenta lectora, mensaje, respuesta, indicador de solicitud de persona, estado de atención y marcas temporales. El modelo actual representa el caso en una fila; no es una tabla independiente por cada mensaje de conversación.
- **Bibliotecario**: identidad propia con username, nombre, apellido, email, hash de contraseña, activo y fecha de creación.

## Relaciones

- `Usuario` 1:N `Prestamo` (la referencia del préstamo puede ser nula).
- `Libro` 1:N `Prestamo` (la referencia del préstamo puede ser nula).
- `Usuario` 1:N `SolicitudPrestamo`.
- `Libro` 1:N `SolicitudPrestamo`.
- Cuenta Django 1:1 `PerfilBiblioteca` y `Usuario` 1:1 `PerfilBiblioteca`.
- Cuenta Django 1:N `MensajeSoporte`.
- `Bibliotecario` es un modelo independiente; el modelo no declara una FK hacia `MensajeSoporte` para registrar quién respondió.

## Reglas y observaciones

1. No debe haber más de un préstamo activo del mismo libro.
2. No se puede crear un préstamo si el libro ya está marcado `Prestado`.
3. Durante un préstamo activo, el estado del libro no debe cambiarse manualmente.
4. La devolución registra fecha y estado `Devuelto`, y deja el libro disponible si no hay otro préstamo activo aplicable.
5. Las relaciones opcionales de `Prestamo` usan `SET_NULL`; por eso se conservan los campos históricos.
6. Las relaciones de `SolicitudPrestamo` usan `PROTECT` para evitar borrar datos referenciados.

El diagrama refleja los campos y relaciones declarados en los modelos, no índices o restricciones adicionales que no estén explícitos en el código.


> Revisión de paquete: 14/10/2026. Ver también `docs/diagramas_y_modelos_2026-10-14.md` y `docs/limite_email_50_2026-10-14.md` para los diagramas editables y el límite actualizado de correo.
