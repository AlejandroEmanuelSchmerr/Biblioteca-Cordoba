# Casos de uso

## Actores
- **Lector:** usuario registrado del portal.
- **Bibliotecario:** personal que administra el funcionamiento bibliotecario.
- **Superusuario:** administrador técnico de Django.
- **Servicio de correo / proveedor de IA:** integraciones opcionales según configuración.

## Casos principales

| ID | Actor | Caso | Resultado esperado |
|---|---|---|---|
| CU-01 | Lector | Registrarse y activar cuenta | Cuenta habilitada según el flujo de activación |
| CU-02 | Lector | Iniciar/cerrar sesión | Sesión propia gestionada de forma segura |
| CU-03 | Lector | Consultar catálogo | Lista de libros y estados disponibles |
| CU-04 | Lector | Solicitar un libro | Solicitud guardada como pendiente |
| CU-05 | Bibliotecario | Resolver solicitud | Solicitud actualizada con estado y nota |
| CU-06 | Bibliotecario | Gestionar usuarios y libros | Registro guardado tras validar los datos |
| CU-07 | Bibliotecario | Registrar préstamo | Libro disponible pasa a prestado y se registra préstamo activo |
| CU-08 | Bibliotecario | Intentar editar estado con préstamo activo | Cambio rechazado |
| CU-09 | Bibliotecario | Registrar devolución | Préstamo cerrado y libro disponible |
| CU-10 | Lector | Consultar comprobante/historial | Solo sus propios registros |
| CU-11 | Lector | Consultar BiblioBot | Respuesta local o de IA si está configurada |
| CU-12 | Lector | Abrir caso de soporte | Caso visible en su historial |
| CU-13 | Bibliotecario | Responder/cerrar soporte | Respuesta e indicador de atención actualizados |
| CU-14 | Superusuario | Administrar configuración y registros | Operación desde el panel administrativo autorizado |

## Excepción central: libro no disponible

Si el libro ya figura como `Prestado` o existe un préstamo activo, el sistema rechaza un nuevo préstamo. Si el préstamo sigue activo, el estado no se modifica manualmente; primero debe registrarse la devolución.
