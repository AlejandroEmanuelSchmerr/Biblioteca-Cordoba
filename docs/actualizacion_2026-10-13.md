# Actualización de Biblioteca Córdoba — 13/10/2026

## Cambios de esta revisión
- BiblioBot incorpora respuestas locales por palabras clave para catálogo, solicitudes, préstamos, comprobantes, acceso, correo, soporte y privacidad. Las respuestas sobre dirección y horario no inventan datos que no estén cargados. La IA externa sigue siendo opcional y requiere `BIBLIOTECA_AI_API_KEY`.
- El comprobante del lector usa una paleta teal/ámbar, encabezado y nomenclatura distintos al comprobante operativo del bibliotecario. El acceso del lector filtra el préstamo por su propia ficha.
- Se explicita el límite de 254 caracteres del email en el formulario de ficha. Los formularios de registro ya declaran `max_length=254` y `maxlength=254`.
- Se agrega un logotipo SVG propio en `backend/biblioteca/static/biblioteca/logo-biblioteca-cordoba.svg`.

## Rutas locales
- Inicio público: `/`
- Registro lector: `/registro/`
- Login lector: `/login/`
- Portal lector: `/mi-cuenta/` (requiere iniciar sesión)
- Login bibliotecario: `/bibliotecario/login/`
- Panel bibliotecario: `/bibliotecario/`
- Bandeja de soporte: `/bibliotecario/soporte/`
- Django Admin del superusuario: `/admin/`

## Base de datos SQL
En desarrollo, Django usa SQLite salvo que se configuren las variables `DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` y `DB_PORT` para PostgreSQL. Antes de producción, usar PostgreSQL administrado, ejecutar migraciones y configurar copias de seguridad. No subir `.env` ni secretos al repositorio.

## Publicación
1. Subir el repositorio a GitHub sin `.env`, contraseñas, base local ni datos reales.
2. Elegir un host compatible con Django/Python y PostgreSQL administrado; configurar variables secretas en el panel del proveedor.
3. Ejecutar `pip install -r requirements.txt`, `python manage.py migrate`, `python manage.py collectstatic --noinput` y crear un superusuario desde consola del proveedor.
4. Configurar dominio propio (un `.com` normalmente no es gratuito; los subdominios del proveedor pueden ser gratuitos), HTTPS, `DEBUG=False`, `ALLOWED_HOSTS`, SMTP y copias de seguridad.
5. Antes de abrir al público, ejecutar tests, `python manage.py check --deploy`, auditoría de dependencias y pruebas de permisos.

## Límites y privacidad
Este proyecto no puede garantizar “cero vulnerabilidades” ni ausencia total de multas. La política legal depende de quién opera el sitio, qué datos reales recoge, analíticas, cookies, proveedores y jurisdicción. Revisar normativa argentina aplicable y pedir asesoramiento legal antes de operar públicamente. Si no hay analítica no esencial, evitar instalar cookies de seguimiento; si se agregan, documentarlas y obtener consentimiento cuando corresponda. La IA puede equivocarse: informar claramente su uso y ofrecer soporte humano.

## Validación pendiente
Esta revisión estática no equivale a una suite de tests ejecutada. En `backend`: `python manage.py check`, `python manage.py test`, `python manage.py check --deploy` en configuración de producción.


## Ajustes BiblioBot y soporte (13/10/2026)

- Las respuestas locales normalizan tildes y signos antes de comparar palabras clave; consultas breves como “libro”, “cuenta”, “cerrar sesión”, “préstamos” y “comprobante” ahora tienen una respuesta específica.
- Se mejoró el mensaje de reserva cuando no hay clave de IA externa configurada: ya no repite el mismo bloque genérico en todas las consultas.
- El portal lector muestra un historial de casos de soporte con estado abierto/cerrado y un detalle desplegable de la conversación.
- El historial de mensajes automáticos se separa de los casos derivados a atención humana para evitar presentar el registro completo del caso como una respuesta automática.
- La IA externa sigue siendo opcional y requiere `BIBLIOTECA_AI_API_KEY`, `BIBLIOTECA_AI_MODEL` y, si corresponde, `BIBLIOTECA_AI_BASE_URL`. Las respuestas por palabras clave funcionan sin esa configuración.

Pendiente de verificación en entorno del proyecto: ejecutar `python manage.py check` y `python manage.py test`; esta edición no afirma que toda la suite haya pasado.


## 13 de octubre de 2026 — Estado protegido durante préstamos y logo institucional

- En la edición de un libro, si existe al menos un préstamo con estado `Activo`, el campo Estado queda deshabilitado y se informa que primero debe registrarse la devolución.
- La protección también se aplica en la validación del formulario del servidor: una petición manipulada no puede cambiar el estado mientras el préstamo siga activo. El estado se mantiene como `Prestado`.
- El flujo normal de devolución sigue siendo el responsable de cerrar el préstamo y cambiar el libro a `Disponible`.
- El logo SVG institucional ahora se muestra en la barra de navegación a través de los archivos estáticos de Django.
- Se actualizan la guía funcional, el diagrama del ciclo del préstamo y el registro de cambios para reflejar la regla.
