# Roles y accesos — Biblioteca Córdoba (14/10/2026)

## Lector
- Se registra en `/registro/`, activa la cuenta si el correo está configurado y accede por `/login/`.
- Su cuenta Django se vincula a `Usuario` mediante `PerfilBiblioteca` (relación uno a uno).
- Puede consultar su información, sus préstamos/solicitudes y sus casos de soporte.

## Bibliotecario
- Usa el modelo propio `Bibliotecario`, no `auth.User`.
- Inicia sesión en `/bibliotecario/login/`. La sesión guarda `bibliotecario_id`; el decorador `bibliotecario_required` recupera al empleado activo antes de permitir vistas de gestión.
- Por eso `Bibliotecario` no tiene FK directa a `Usuario`, `Libro` o `Prestamo`: su relación con los módulos es a través de la capa de vistas/rutas protegidas y de la sesión. En el diagrama de arquitectura debe conectarse al bloque de autenticación y vistas, no dibujarse una FK inventada en el ERD.

## Superusuario
- Es una cuenta Django con `is_superuser=True` y `is_staff=True`; el panel `/admin/` comprueba permisos de superusuario.
- Gestiona modelos y cuentas desde Django Admin.

## Importante
Los roles no comparten el mismo mecanismo de autenticación: lector y administrador usan `auth.User`; el bibliotecario usa el modelo propio `Bibliotecario` y una sesión separada. No afirmar que las identidades estén en bases de datos físicamente separadas: conviven en la misma base de datos.
