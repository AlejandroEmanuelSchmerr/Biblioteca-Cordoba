# Revisión funcional y de privacidad — 12/10/2026

## Cambios de esta entrega
- Se agregó un cierre explícito de caso de soporte tanto para el lector como para el bibliotecario. Una respuesta individual del bibliotecario ya no marca automáticamente el caso como cerrado.
- Mientras el caso humano está abierto, los nuevos mensajes del lector se agregan al caso existente y no pasan por BiblioBot, evitando respuestas mezcladas. El modelo actual conserva la conversación en campos de texto agregados; para un sistema de producción conviene migrar a una tabla `MensajeConversacion` con una fila por mensaje, autor y fecha.
- Las tarjetas de préstamos activos y solicitudes ahora enlazan a sus secciones.
- Se agregaron páginas informativas de privacidad, términos, cookies y reembolsos. Son textos iniciales y deben revisarse con asesoramiento legal antes de publicar.
- BiblioBot tiene una respuesta local con funciones conocidas del sistema y no debe inventar horarios, dirección o reglas no configuradas. Para respuestas generativas reales se requiere configurar `BIBLIOTECA_AI_API_KEY`, endpoint y modelo.

## Cookies y consentimiento
La aplicación usa cookies técnicas de sesión y CSRF. No se detecta analítica publicitaria configurada en este código. Las cookies estrictamente necesarias normalmente se tratan distinto de las cookies de analítica/marketing; antes de agregar servicios de terceros, revisar la normativa aplicable y solicitar consentimiento cuando corresponda. No se puede garantizar ausencia de multas con un cambio de código.

## Datos mínimos y terceros
- Recopilar únicamente datos necesarios para la cuenta, préstamos y soporte. Revisar si el teléfono es imprescindible.
- Revisar el proveedor SMTP y el proveedor de IA: ambos pueden procesar datos fuera de la aplicación. No enviar DNI, correos ni historial personal al modelo si no es imprescindible; la integración actual debe revisarse para minimización.
- No hay pagos en esta versión: política de reembolsos informa que no se procesa dinero.
- Verificar licencias y permisos de las portadas, iconos y recursos visuales; preferir imágenes propias o con licencia documentada.
- Revisar contraste WCAG, navegación por teclado, etiquetas, textos alternativos y formularios en dispositivos reales.

## No verificado todavía
No se ejecutaron los tests completos de Django ni una auditoría legal externa en este entorno. Antes de producción: `python manage.py check`, `python manage.py test`, `python manage.py check --deploy`, `pip-audit`, revisión manual de permisos, SMTP/IA y pruebas de accesibilidad. No presentar el sitio como “cero vulnerable” ni como certificado legal.
