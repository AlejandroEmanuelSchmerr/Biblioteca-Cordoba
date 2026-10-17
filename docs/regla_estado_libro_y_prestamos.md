# Regla de negocio: estado de un libro con préstamo activo

## Regla
Un libro asociado a un préstamo cuyo estado es `Activo` debe permanecer en `Prestado`. El bibliotecario puede modificar los demás datos bibliográficos, pero no cambiar el estado manualmente mientras el préstamo esté activo.

## Comportamiento esperado
1. Al crear un préstamo, el sistema registra el préstamo como `Activo` y el libro como `Prestado`.
2. Al editar un libro prestado, el campo Estado aparece bloqueado y explica por qué.
3. La validación del servidor conserva `Prestado` aunque se envíe una petición manipulada.
4. Al registrar la devolución, el préstamo pasa a `Devuelto` y el sistema cambia el libro a `Disponible`.
5. No se debe borrar un libro que tenga préstamos activos.

## Criterios de aceptación
- [ ] Con un préstamo activo, el estado no se puede cambiar desde la pantalla de edición.
- [ ] Una petición POST manipulada tampoco cambia el estado.
- [ ] Tras registrar la devolución, el libro queda disponible según el flujo de devolución.
- [ ] Un libro sin préstamo activo puede seguir el flujo normal de edición de estado.

## Archivos relacionados
- `backend/biblioteca/forms.py`: bloqueo y validación del formulario.
- `backend/biblioteca/views.py`: creación y devolución de préstamos.
- `backend/biblioteca/models.py`: estados y relaciones.
- `diagramas/Diagrama_Flujo_Prestamo.drawio`: flujo visual del préstamo.
