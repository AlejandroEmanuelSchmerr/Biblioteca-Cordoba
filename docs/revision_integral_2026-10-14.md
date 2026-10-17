# Revisión integral — 14/10/2026

## Hallazgo sobre Bibliotecario
El modelo `Bibliotecario` no está desconectado del sistema funcional: el acceso se conecta por sesión `bibliotecario_id` y `bibliotecario_required` a las vistas protegidas. No hay FK de `Bibliotecario` a `Libro`, `Usuario` o `Prestamo`, por lo que se documenta en arquitectura y no como relación ER.

## Corrección de devolución
El orden anterior intentaba guardar el libro como Disponible mientras el préstamo aún estaba Activo. Ahora se persiste primero el préstamo como Devuelto y luego se guarda el libro como Disponible, dentro de `transaction.atomic()`. `Libro.clean()` también rechaza cambios de estado si existen préstamos activos. El admin muestra estado como solo lectura en ese caso.

## Límites
Se agregó inventario de longitudes y reglas. `max_length` y `maxlength` deben revisarse conjuntamente; `maxlength` por sí solo no protege la aplicación.

## Validación pendiente
Se validó sintaxis de Python, XML de los diagramas y apertura del ZIP. No se ejecutaron pruebas Django en esta sesión; ejecutar comandos del README antes del despliegue.
