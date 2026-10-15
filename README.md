# SkiOx Dashboard

A group-project dashboard for presenting and managing status data for the SkiOx emergency oxygen delivery system concept. The repository contains a Django web application and REST API, plus a separate lightweight Python HTTP-server prototype in `app.py`.

> **Demonstration software:** This project does not itself connect to or control medical hardware. The dashboard and sample records are for software demonstration and coursework; they are not a medical device or a substitute for clinical monitoring.

## Problem and objectives

An emergency oxygen system needs a clear way to view component state, oxygen-system state, battery information, sensor readings, alerts, and system logs. SkiOx Dashboard provides web pages and API endpoints for recording and reviewing those data. The current repository demonstrates the software layer; the code does not include an ESP32 firmware project or a verified live sensor connection.

## Features

- Django dashboard pages for system overview, components, sensor data, alerts, and logs.
- Django REST Framework endpoints for component status, SpO2 and heart-rate readings, system state, battery status, alerts, logs, and a summary.
- SQLite-backed Django models and Django admin.
- Sample-data loader for local demonstrations.
- Responsive templates using Bootstrap assets from CDNs.
- A separate standard-library server in `app.py` on port 8001, with its own SQLite schema. It is a prototype distinct from the Django app.

## Technology stack

**Django application:** Python, Django 5.0.1, Django REST Framework 3.14.0, SQLite, Django templates, JavaScript, and custom CSS. `django-cors-headers` is installed and configured. The templates load Bootstrap 5.3, Bootstrap Icons 1.10, Chart.js 3.9, and Axios from CDNs.

**Standalone prototype:** Python standard library modules (`http.server`, `socketserver`, `sqlite3`, and related modules). It does not use the Django dependencies.

Exact Python packages and versions for the Django application are listed in [`requirements.txt`](requirements.txt).

## Architecture

```text
Browser
  ├── Django templates + static CSS/JavaScript
  └── REST calls ──> Django URL router ──> views / DRF viewsets
                                           ├── serializers
                                           └── Django models ──> SQLite (db.sqlite3)

Separate prototype: browser ──> app.py HTTP server ──> SQLite (skiox_data.db)
```

The Django application is the recommended path for setup and demonstration. The standalone `app.py` prototype is independent and does not share the Django database or API implementation.

## Setup and run (Django application)

Requirements: Python with support for the pinned Django 5.0.1 release and `pip`. The project checks passed in the available Python 3.14 environment.

```bash
git clone https://github.com/Riteshyadav3635/SKiOx-Dashboard-.git
cd SKiOx-Dashboard-
python3 -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py shell < load_sample_data.py   # Optional demo records
python manage.py runserver
```

Open <http://127.0.0.1:8000/>. Create an admin account with `python manage.py createsuperuser`, then visit <http://127.0.0.1:8000/admin/>. The sample-data loader can be run again; it uses `get_or_create` for its records.

The simple `run.sh` script starts this Django development server. To run the standalone prototype instead, activate a Python environment and run `python app.py`; it listens on port 8001 and creates `skiox_data.db` in the current directory.

## Environment configuration

For local development, Django defaults to debug mode, localhost hosts, and the repository's SQLite database. These defaults are for local use only. Settings can be overridden with environment variables:

| Variable | Purpose | Local default |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | Django signing key | Local-only development value; set a private value outside local development |
| `DJANGO_DEBUG` | Enable Django debug mode (`true`/`false`) | `true` |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated allowed host names | `localhost,127.0.0.1` |
| `DJANGO_CORS_ALLOWED_ORIGINS` | Comma-separated CORS origins | Localhost ports 3000 and 8000 |

Example for local shell use:

```bash
export DJANGO_SECRET_KEY="$(python -c 'from secrets import token_urlsafe; print(token_urlsafe(48))')"
export DJANGO_DEBUG=true
export DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
```

Do not commit local `.env` files or production secrets. The repository uses SQLite by default; PostgreSQL and Redis are not configured as Django data services.

## API overview

The Django API is mounted under `/api/`. DRF routers provide endpoints for `/components/`, `/sensors/`, `/system/`, `/battery/`, `/alerts/`, and `/logs/`; the dashboard summary is at `/api/summary/`. Viewset actions include current/latest status, statistics, unresolved alerts, alert resolution, and oxygen-delivery state updates. These are software data operations; they do not actuate physical hardware.

## Screenshots

No screenshots are currently included. Add reviewed screenshots under `docs/screenshots/` and link them here before publishing a visual portfolio presentation.

## Group project and attribution

This is a group project. The available Git history records:

- **Anup Kumar** (`01-anupkr`): authored the initial project commit, which added the application and project files.
- **Ritesh Kumar Yadav** (`Riteshyadav3635`): authored the commit adding the initial Django database migration.

These credits describe the commits visible in this repository; the available history does not establish further task-level responsibilities. Original project attribution to Anup and the group context are retained.

## Future improvements

- Connect and validate a real sensor/firmware data source before describing readings as live.
- Add automated tests for Django views, API behavior, and data validation.
- Add authentication and authorization for state-changing API endpoints.
- Align or retire the separate `app.py` prototype and make the supported run path unambiguous.
- Add verified screenshots and deployment documentation after those workflows are tested.

## Project documentation

Additional project notes are available in [`API_DOCUMENTATION.md`](API_DOCUMENTATION.md), [`QUICK_START.md`](QUICK_START.md), and the other documentation files. Treat older deployment and feature claims as historical notes where they conflict with the current source code.
