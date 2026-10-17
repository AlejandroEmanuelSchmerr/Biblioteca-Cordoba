# Requisitos funcionales — versión consolidada

## Gestión y autenticación
- RF-01: el sistema debe permitir el acceso del bibliotecario mediante su pantalla de inicio de sesión.
- RF-02: el lector debe poder registrarse, activar su cuenta y acceder a su portal.
- RF-03: el superusuario debe poder acceder al panel administrativo de Django.
- RF-04: el sistema debe impedir el acceso a funciones no autorizadas según el rol.

## Catálogo y lectores
- RF-05: el bibliotecario debe crear, consultar, buscar, editar y eliminar fichas de usuarios de biblioteca según las reglas de integridad.
- RF-06: el bibliotecario debe crear, consultar, buscar, filtrar, editar y eliminar libros cuando no existan restricciones por préstamos.
- RF-07: el catálogo debe mostrar el estado de cada libro.

## Préstamos
- RF-08: el bibliotecario debe registrar un préstamo para un libro disponible y un lector válido.
- RF-09: el sistema debe impedir prestar un libro marcado como prestado o con otro préstamo activo.
- RF-10: al registrar el préstamo, el libro debe pasar a `Prestado`.
- RF-11: mientras exista un préstamo activo, el estado del libro no debe poder modificarse manualmente.
- RF-12: al registrar la devolución, el préstamo debe pasar a `Devuelto`, guardar la fecha de devolución y actualizar el libro a `Disponible`.
- RF-13: el sistema debe conservar el historial y permitir consultar/generar comprobantes cuando corresponda.

## Portal, solicitudes y soporte
- RF-14: el lector debe consultar sus propios préstamos, solicitudes y comprobantes, sin acceder a los datos de otros lectores.
- RF-15: el lector debe solicitar un libro y consultar el estado de la solicitud.
- RF-16: el bibliotecario debe revisar y responder solicitudes.
- RF-17: el lector debe consultar BiblioBot y derivar consultas a soporte humano.
- RF-18: el lector debe ver su historial de casos de soporte y su estado.
- RF-19: el personal autorizado debe responder y cerrar casos de soporte.

Los requisitos deben contrastarse con las vistas, formularios y pruebas de la versión que se publique. Un requisito escrito no demuestra por sí solo que esté implementado.
