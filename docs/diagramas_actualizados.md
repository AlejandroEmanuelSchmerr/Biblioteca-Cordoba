# Guía de diagramas actualizados

## 1. Diagrama entidad-relación

El nuevo ER debe mostrar las entidades reales de `models.py`: `Usuario`, `Libro`, `Prestamo`, `PerfilBiblioteca`, `SolicitudPrestamo`, `MensajeSoporte` y `Bibliotecario`. Debe representar que `PerfilBiblioteca` une una cuenta Django y una ficha de biblioteca; el modelo `Bibliotecario` es independiente; y `MensajeSoporte` actualmente pertenece a una cuenta Django y guarda el texto de la respuesta dentro de la misma fila. No dibujar una tabla de mensajes individuales ni una relación de bibliotecario con soporte que no esté declarada en los modelos.

`Prestamo.dni` y `Prestamo.id_libro` son referencias anulables (`SET_NULL`); el registro conserva copias históricas del lector y del libro. Las solicitudes usan `PROTECT` para lector y libro.

## 2. Diagrama de flujo de préstamo

Debe reflejar: seleccionar lector/libro → comprobar estado y préstamos activos → rechazar si no está disponible → registrar préstamo → marcar libro como prestado → esperar devolución → registrar fecha y cerrar préstamo → marcar libro disponible → conservar historial.

La regla de bloqueo del estado manual debe aparecer como nota o rama: **con préstamo activo, no permitir cambiar manualmente el estado del libro**. El control debe existir en la interfaz y en el servidor.

## 3. Arquitectura y roles

Separar lector, bibliotecario y superusuario Django. El lector usa cuenta Django vinculada a `Usuario` por `PerfilBiblioteca`; el bibliotecario usa el modelo independiente `Bibliotecario`; el superusuario entra por Django Admin. Desde los roles se conectan a las rutas y módulos que corresponden.

## Archivos editables

- `Diagrama_Entidad_Relacion.drawio`
- `Diagrama_Flujo_Prestamo.drawio`
- `modelo_datos_actualizado_2026-10-13.mmd`
- `flujo_prestamo.mmd`
- `arquitectura_roles_y_rutas.mmd`


> Revisión de paquete: 14/10/2026. Ver también `docs/diagramas_y_modelos_2026-10-14.md` y `docs/limite_email_50_2026-10-14.md` para los diagramas editables y el límite actualizado de correo.
