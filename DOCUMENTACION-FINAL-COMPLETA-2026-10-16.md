# Biblioteca Córdoba — Documentación técnica final

**Fecha de revisión documental:** 16 de octubre de 2026  
**Raíz del repositorio:** `Biblioteca-2026/`  
**Backend Django:** `Biblioteca-2026/backend/`

Este documento resume la estructura, los roles, los modelos, las reglas funcionales y los pasos de publicación. Es documentación del proyecto; no constituye una auditoría de seguridad ni reemplaza las pruebas en el entorno de destino.

## 1. Descripción

Biblioteca Córdoba es una aplicación web de gestión bibliotecaria desarrollada con Python y Django. Incluye gestión del catálogo, fichas de lectores, préstamos y devoluciones, historial y comprobantes PDF, solicitudes de préstamo, portal del lector y soporte. BiblioBot ofrece respuestas locales y puede integrarse con un proveedor externo de IA cuando se configura.

## 2. Tecnologías y dependencias

- Python y Django (la versión fijada en `requirements.txt` es la referencia para instalar el proyecto).
- Django Templates, HTML, CSS/Bootstrap y JavaScript.
- ORM de Django; SQLite para desarrollo y PostgreSQL configurable para producción.
- ReportLab para comprobantes PDF y Pillow para imágenes de portada.
- `python-dotenv` para cargar variables locales desde `backend/.env`.
- diagrams.net y Mermaid para diagramas editables y sus fuentes.

Las dependencias están declaradas en `requirements.txt`, ubicado en la raíz `Biblioteca-2026/`.

## 3. Roles e identidades

### Lector

El lector utiliza una cuenta de autenticación de Django vinculada a una ficha `Usuario` mediante `PerfilBiblioteca`. Las vistas del portal deben restringir los préstamos, solicitudes y casos de soporte a los registros correspondientes a la cuenta autenticada.

### Bibliotecario

`Bibliotecario` es un modelo propio, independiente del modelo de autenticación de Django. El acceso de trabajo se basa en una sesión de aplicación y en la comprobación de que la cuenta esté activa. No se debe representar como una FK a las tablas del catálogo si esa FK no está declarada en los modelos. Las referencias de auditoría opcionales existentes se documentan en el apartado de relaciones.

### Superusuario

El superusuario es una cuenta de Django con permisos de administración para `/admin/`. No equivale a una cuenta de bibliotecario ni a una ficha de lector.

## 4. Modelos y relaciones

Los modelos de la aplicación incluyen `Usuario`, `Libro`, `Prestamo`, `PerfilBiblioteca`, `SolicitudPrestamo`, `MensajeSoporte` y `Bibliotecario`, además del modelo de cuenta de Django. Para el detalle de campos, tipos y restricciones, consultar `backend/biblioteca/models.py`, las migraciones y `docs/base_de_datos.md`.

Relaciones principales documentadas:

- `Usuario` puede tener múltiples préstamos; la referencia actual del préstamo puede ser nula para preservar el historial.
- `Libro` puede aparecer en múltiples préstamos históricos; la referencia puede ser nula para preservar registros históricos.
- `Usuario` y `Libro` se relacionan con solicitudes de préstamo. Las referencias protegidas impiden eliminar registros que estén referenciados por solicitudes.
- `PerfilBiblioteca` vincula una cuenta Django y una ficha `Usuario` mediante relaciones uno a uno.
- `MensajeSoporte` pertenece a una cuenta de Django. El modelo conserva el caso y su respuesta en los campos definidos actualmente; no debe documentarse como un sistema de mensajes individuales normalizados si esa estructura no está implementada.
- `Prestamo`, `SolicitudPrestamo` y `MensajeSoporte` incluyen referencias opcionales de auditoría a `Bibliotecario` donde así lo indican los modelos actuales.

Para diagramas, utilizar los archivos reales de `diagramas/` y la guía `diagramas/LEEME_DIAGRAMAS_FINAL_2026-10-15.md`. Las relaciones de un diagrama deben corresponder a relaciones reales del ORM.

## 5. Reglas funcionales importantes

- Un libro no debe prestarse si ya tiene un préstamo activo o no está disponible.
- Mientras exista un préstamo activo, no se debe permitir cambiar manualmente el estado del libro de forma incompatible con ese préstamo.
- Al registrar una devolución, el préstamo pasa a `Devuelto`, se registra la fecha y el libro vuelve a `Disponible` según las reglas del sistema.
- El historial y los datos históricos del comprobante deben conservarse aunque se elimine una referencia opcional.
- Las solicitudes de préstamo tienen estados `Pendiente`, `Aprobada` y `Rechazada`.
- Los casos de soporte deben mantener un estado coherente; responder un caso no debe equivaler automáticamente a cerrarlo si el flujo requiere un cierre explícito.
- BiblioBot puede responder con lógica local. La integración de IA externa depende de las variables y credenciales configuradas y puede producir errores; no se deben enviar datos personales innecesarios al proveedor.

## 6. Migraciones y base de datos

Las migraciones versionadas se encuentran en `backend/biblioteca/migrations/`. La migración `0011_alter_usuario_dni_alter_usuario_telefono.py` modifica los campos `Usuario.dni` y `Usuario.telefono`: DNI de ocho dígitos y teléfono de uno a doce dígitos según los validadores declarados.

El estado aplicado de una migración depende de cada base de datos local o remota. Comprobarlo con `python manage.py showmigrations biblioteca`. Antes de aplicar cambios sobre una base con datos, hacer una copia de seguridad y revisar que los datos existentes sean compatibles.

En desarrollo, la configuración por defecto utiliza SQLite en `backend/db.sqlite3`. Para producción, configurar una base persistente como PostgreSQL mediante las variables de entorno soportadas por `backend/config/settings.py`. No subir bases locales ni copias de seguridad al repositorio.

## 7. Estructura del repositorio

```text
Biblioteca-2026/
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
├── DOCUMENTACION-FINAL-COMPLETA-2026-10-16.md
├── backend/
│   ├── config/
│   ├── biblioteca/
│   │   ├── migrations/
│   │   ├── templates/
│   │   └── static/
│   └── manage.py
├── diagramas/
├── docs/
└── requisitos_iniciales/
```

## 8. Instalación local en Windows

Ejecutar desde la raíz `Biblioteca-2026/`, donde se encuentra `requirements.txt`.

```powershell
py -m venv backend\venv
.\backend\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example backend/.env
```

Completar `backend/.env` con los valores apropiados para el entorno local. No compartirlo ni subirlo a GitHub. Luego entrar al backend y ejecutar los comandos: 

```powershell
cd backend
python manage.py migrate
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
python manage.py runserver
```

Abrir `http://127.0.0.1:8000/`. Si se necesita acceso a `/admin/` y no existe un superusuario, ejecutar `python manage.py createsuperuser`.

## 9. Pruebas y estado de verificación

Las pruebas automatizadas se ejecutan con `python manage.py test` desde `backend/`. `python manage.py check` valida aspectos generales del proyecto, y `python manage.py makemigrations --check --dry-run` comprueba si hay cambios de modelos que no estén reflejados en migraciones.

El archivo `docs/pruebas.md` contiene casos manuales recomendados. No se debe presentar un plan de pruebas como evidencia de que cada caso manual fue completado. Registrar resultados junto con fecha, versión y entorno cuando se realicen pruebas.

## 10. Documentación complementaria

- `README.md`: presentación del proyecto e instalación rápida.
- `arquitectura.md` y `backend_estructura.md`: arquitectura y ubicación de los componentes.
- `docs/funcionamiento.md`: flujos funcionales.
- `docs/base_de_datos.md` y `relaciones.md`: modelos y relaciones.
- `docs/pruebas.md`: pruebas automatizadas y manuales.
- `docs/seguridad_y_despliegue.md`: preparación para producción.
- `LIMITES_CAMPOS_Y_VALIDACIONES.md`: límites y reglas documentadas de los campos.
- `diagramas/`: diagramas editables, fuentes Mermaid y guía de lectura.
- `requisitos_iniciales/`: requisitos y casos de uso iniciales.

## 11. Preparación para GitHub

Antes de subir el proyecto, revisar el resultado de `git status --short` y confirmar que no se incluyan `.env`, bases SQLite, copias de seguridad, entornos virtuales, archivos `.pyc`, credenciales o datos personales. El archivo `.gitignore` contiene reglas para excluir estos elementos, pero no elimina archivos ya rastreados por Git ni los filtra automáticamente si se suben manualmente desde la web.

## 12. Preparación para producción

Antes de publicar en internet:

1. Configurar secretos mediante variables de entorno del proveedor de hosting.
2. Establecer `DJANGO_DEBUG=False`, `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS` y `DJANGO_CSRF_TRUSTED_ORIGINS` para el dominio real.
3. Configurar PostgreSQL persistente, correo, archivos estáticos y almacenamiento de portadas.
4. Ejecutar migraciones, `python manage.py check --deploy`, pruebas automatizadas y pruebas manuales de roles y flujos críticos.
5. Confirmar HTTPS, permisos, copias de seguridad y procedimiento de restauración.
6. Usar cuentas de prueba; no importar datos personales reales sin revisar necesidad, privacidad y seguridad.
7. Revisar las páginas legales incluidas: son textos iniciales, no asesoramiento ni certificación jurídica.

Los servicios gratuitos pueden suspender aplicaciones, limitar recursos o eliminar bases de datos después de cierto plazo. Revisar las condiciones vigentes del proveedor antes de depender del alojamiento para datos persistentes.

## 13. Alcance y limitaciones

Este documento describe la estructura y el comportamiento previstos del proyecto. No afirma que el sistema sea invulnerable, que haya superado una auditoría externa ni que todas las pruebas manuales se hayan completado. Antes de usarlo con usuarios reales, verificar los flujos en el entorno publicado y revisar seguridad, privacidad, accesibilidad, licencias y requisitos legales aplicables.
