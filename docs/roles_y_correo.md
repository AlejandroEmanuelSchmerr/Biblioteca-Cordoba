# Roles de acceso y correo real

## Administrador principal

El superusuario administra el sistema desde `/admin/` (Django Admin). Solo una cuenta activa con `is_superuser=True` puede entrar a ese panel. Desde allí puede administrar usuarios, grupos, fichas, libros, préstamos, solicitudes y soporte.

## Bibliotecario

El bibliotecario entra por `/bibliotecario/login/`. Su cuenta debe ser creada por el superusuario en Django Admin → Usuarios → Añadir usuario. Debe tener `Activo` y `Estado del personal` habilitados, y `Estado de superusuario` deshabilitado. No se debe marcar como superusuario. Las vistas operativas de la biblioteca exigen una cuenta de personal que no sea superusuario; Django Admin queda reservado al administrador principal.

## Lector

El lector se registra en `/registro/` e inicia sesión en `/login/`. La cuenta permanece inactiva hasta confirmar el correo. La autenticación de lectores rechaza cuentas de personal.

## Configurar envío de correos

Copiar `.env.example` a `.env` en la raíz `Biblioteca-2026/` y completar `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` y `DEFAULT_FROM_EMAIL`. El proyecto usa SMTP como backend predeterminado y no imprime los enlaces de activación ni recuperación en la consola. Para Gmail, activar la verificación en dos pasos y usar una contraseña de aplicación; nunca usar la contraseña habitual de la cuenta. Mantener `.env` fuera de Git.

Sin credenciales SMTP válidas, el registro no puede enviar el mensaje y mostrará un error genérico. Eso es intencional: no se debe activar la cuenta ni mostrar un enlace secreto en la consola como sustituto del correo.
