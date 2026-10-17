# Funcionamiento del sistema

## Área del bibliotecario

El personal inicia sesión en su acceso propio y puede gestionar fichas de usuarios, catálogo de libros, préstamos, devoluciones, historial y comprobantes. También puede revisar solicitudes de préstamo y atender casos de soporte.

## Portal del lector

El lector registra una cuenta, la activa según el flujo de correo configurado y accede a su portal. Desde allí consulta el catálogo, solicita libros y revisa el estado de sus solicitudes, sus préstamos/comprobantes y sus casos de soporte.

## Ciclo de préstamo

1. El bibliotecario elige un lector y un libro disponible.
2. El sistema valida que el libro no esté prestado y que no exista otro préstamo activo para ese libro.
3. Al guardar el préstamo, el libro pasa a `Prestado`.
4. Mientras el préstamo esté activo, la edición manual del estado debe estar bloqueada tanto en la interfaz como en el servidor.
5. Al registrar la devolución, el préstamo pasa a `Devuelto`, se registra la fecha y el libro vuelve a `Disponible`.
6. El historial y los datos históricos del comprobante se conservan.

## BiblioBot y soporte

BiblioBot ofrece respuestas locales por coincidencia de palabras clave y puede recurrir a un proveedor de IA si está configurado. La calidad de la respuesta depende de la lógica local, del contexto enviado y de la disponibilidad/configuración de la API; no debe describirse como un sistema que conoce automáticamente toda la información. Los casos derivados a una persona deben poder revisarse en el historial y cerrarse explícitamente.
