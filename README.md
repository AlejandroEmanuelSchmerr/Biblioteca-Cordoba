# Biblioteca Córdoba

Sistema web de gestión bibliotecaria desarrollado con Python y Django. Incluye un área de gestión para bibliotecarios y un portal de lectores con catálogo, solicitudes de préstamo, consulta de préstamos y comprobantes, y soporte.

## Funcionalidades principales

- Accesos diferenciados para lectores, bibliotecarios y superusuario de Django.
- Gestión de fichas de lectores y catálogo de libros, con búsquedas y filtros.
- Registro de préstamos, devoluciones, historial y comprobantes PDF.
- Validaciones para impedir préstamos duplicados y cambios manuales incompatibles con préstamos activos.
- Portal del lector, solicitudes de préstamo y seguimiento de solicitudes.
- BiblioBot con respuestas locales y posibilidad de integrar un proveedor externo de IA mediante configuración.
- Casos de soporte con respuestas y cierre explícito.
- Formularios, controles de acceso y documentación técnica.

## Tecnologías

Python, Django, Django Templates, HTML, CSS, Bootstrap, JavaScript, ORM de Django, SQLite para desarrollo, PostgreSQL para producción, ReportLab para comprobantes PDF, Pillow para portadas, Git y GitHub.

## Estructura del proyecto

La raíz del repositorio es `Biblioteca-2026/`.

```text
Biblioteca-2026/
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
├── backend/
│   ├── config/              # configuración y rutas globales
│   ├── biblioteca/          # modelos, vistas, formularios, URLs, pruebas
│   ├── templates/           # plantillas globales, si corresponde
│   └── manage.py
├── diagramas/               # diagramas editables y fuentes Mermaid
├── docs/                    # funcionamiento, datos, pruebas y despliegue
├── requisitos_iniciales/    # requisitos y casos de uso
└── DOCUMENTACION-FINAL-COMPLETA-2026-10-16.md
```

## Instalación local en Windows

Los comandos siguientes se ejecutan desde la raíz `Biblioteca-2026/`, donde está este README y `requirements.txt`.

### 1. Crear y activar el entorno virtual

```powershell
py -m venv backend\venv
.\backend\venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación, se puede ejecutar la ruta del intérprete directamente como alternativa o ajustar la política solo para la sesión siguiendo la documentación oficial de Python/PowerShell.

### 2. Instalar dependencias

```powershell
python -m pip install -r requirements.txt
```

### 3. Configurar variables de entorno

La configuración Django busca el archivo `backend/.env`. Copiá la plantilla de la raíz y completá los valores localmente:

```powershell
Copy-Item .env.example backend/.env
```

Revisá `backend/.env` y reemplazá cualquier valor de ejemplo según tu entorno. No publiques ese archivo ni compartas credenciales reales. Si una variable no se necesita para desarrollo, dejala como indique la plantilla y la configuración del proyecto.

### 4. Ejecutar migraciones y comprobaciones

```powershell
cd backend
python manage.py migrate
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

### 5. Iniciar el servidor local

```powershell
python manage.py runserver
```

Abrí `http://127.0.0.1:8000/` en el navegador.

Para crear una cuenta de superusuario de Django y acceder a `/admin/`, si todavía no existe una:

```powershell
python manage.py createsuperuser
```

El bibliotecario tiene un acceso separado en `/bibliotecario/login/`; el lector usa el flujo de registro e inicio de sesión del portal. Consultá `backend/biblioteca/urls.py` y `backend/config/urls.py` para las rutas definidas en esta versión.

## Pruebas

Desde `backend/`, con el entorno virtual activado:

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

La documentación de pruebas describe los casos automatizados y manuales previstos. Los resultados deben atribuirse a una ejecución concreta en el entorno correspondiente; este README no afirma que todas las pruebas manuales se hayan completado.

## Configuración sensible y seguridad

- Usá `.env.example` como plantilla y guardá los valores reales en `backend/.env` o en variables de entorno del proveedor de hosting.
- Nunca subas `.env`, contraseñas, claves SMTP, tokens, claves de API ni datos personales reales.
- No subas la base de datos local `backend/db.sqlite3`, sus copias de seguridad ni el entorno virtual.
- Para producción configurá `DEBUG=False`, `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `DJANGO_CSRF_TRUSTED_ORIGINS`, base de datos persistente, HTTPS, correo, archivos estáticos y copias de seguridad.
- Revisá `docs/seguridad_y_despliegue.md` y ejecutá `python manage.py check --deploy` con la configuración de producción real.

## Documentación y diagramas

- `DOCUMENTACION-FINAL-COMPLETA-2026-10-16.md`: resumen técnico general y guía de cierre.
- `arquitectura.md` y `backend_estructura.md`: componentes y estructura del código.
- `docs/`: funcionamiento, base de datos, roles, pruebas, seguridad y despliegue.
- `requisitos_iniciales/`: requisitos y casos de uso.
- `diagramas/`: diagramas editables `.drawio`, fuentes Mermaid `.mmd` y su archivo LEEME.
- `LIMITES_CAMPOS_Y_VALIDACIONES.md`: límites y reglas de validación documentados.

## Alcance y estado

Biblioteca Córdoba es un proyecto de portfolio y desarrollo. Antes de utilizarlo con datos reales, verificá los flujos completos, los permisos por rol, el correo, los archivos subidos, las copias de seguridad y la configuración de producción. Las páginas legales incluidas son material inicial y requieren revisión profesional según la jurisdicción y el uso real.

## Qué voy a utilizar y demostrar

Python, Django, ORM, modelos y relaciones, CRUD, formularios, validaciones, autenticación y autorización, consultas, plantillas, generación de PDF, pruebas automatizadas, Git/GitHub y documentación técnica.
