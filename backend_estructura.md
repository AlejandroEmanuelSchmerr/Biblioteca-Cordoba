# Estructura del backend

La raíz del repositorio es `Biblioteca-2026/`. El proyecto Django está dentro de `backend/`.

## Archivos principales

- `requirements.txt`: dependencias del proyecto; está en la raíz del repositorio.
- `backend/manage.py`: punto de entrada para comandos de Django.
- `backend/config/settings.py`: configuración general.
- `backend/config/urls.py`: rutas globales.
- `backend/biblioteca/models.py`: modelos de datos.
- `backend/biblioteca/forms.py`: formularios y validaciones.
- `backend/biblioteca/views.py`: lógica de vistas.
- `backend/biblioteca/urls.py`: rutas de la aplicación.
- `backend/biblioteca/admin.py`: configuración del panel Django.
- `backend/biblioteca/tests.py`: pruebas automatizadas, si están definidas en este archivo.
- `backend/biblioteca/templates/`: plantillas de la aplicación.
- `backend/biblioteca/static/`: CSS, JavaScript e imágenes estáticas de la aplicación.
- `backend/biblioteca/migrations/`: migraciones de base de datos.

## Variables de entorno

Django carga la configuración local desde `backend/.env`. El repositorio incluye `.env.example` en la raíz como plantilla; copiá esa plantilla a `backend/.env` y completá los valores localmente. No publiques `backend/.env`.

## Base de datos

En desarrollo, SQLite se almacena en `backend/db.sqlite3` y se excluye del repositorio. En producción, configurá una base persistente, por ejemplo PostgreSQL, mediante las variables documentadas en `backend/config/settings.py` y `docs/seguridad_y_despliegue.md`.
