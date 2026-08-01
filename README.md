# Digital-auto-service

Multi-tenant web app for running an auto-repair business. An owner registers, verifies their email, and manages six areas: managers, clients, cars, orders, stations, and workers. Owners invite managers, who work inside the owner's company with the same data, minus manager administration and station create/delete. A PDF company report and a small token-auth REST API for manager accounts are included.

Built with Django 5.2, PostgreSQL (psycopg 3), Django REST Framework, and xhtml2pdf. Configuration comes from a `.env` file via django-environ.

## Requirements

- Python 3.11
- PostgreSQL (any recent version; developed against 17)

## Setup

1. Create and activate a virtualenv, then install dependencies:

   ```sh
   python3.11 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Create the database:

   ```sh
   createdb DAS_db
   ```

3. Create your `.env` from the example and adjust it:

   ```sh
   cp .env.example .env
   ```

   - `SECRET_KEY` — any long random string.
   - `DATABASE_URL` — `postgres://USER:PASSWORD@HOST:PORT/DAS_db` (the example assumes a local `postgres` role with trust auth).
   - Email: the default `EMAIL_BACKEND` prints emails to the console, which is all you need locally — verification and invite links appear in the runserver output. For real sending, set `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend` and fill in the `EMAIL_*` variables.

4. Apply migrations and run:

   ```sh
   python manage.py migrate
   python manage.py runserver
   ```

   The app is at http://127.0.0.1:8000/.

## Roles

- **Owner** — self-registers at `/register/`, verifies email, then manages everything under `/dashboard/`. Owners create managers, who receive an invite email with a set-your-password link.
- **Manager** — works with the owner's clients, cars, orders, workers, and stations; cannot manage other managers, cannot create or delete stations, and can edit only stations they own.

Deletion follows the dependency chain: anything referenced by other records (a client with cars, a station with orders) must have its dependents removed first.

## Django admin

The admin at `/admin/` is internal tooling for a superuser; it is not tenant-scoped and is never handed to owners or managers. Create a superuser with:

```sh
python manage.py createsuperuser
```

All seven models (accounts, email verifications, clients, cars, orders, stations, workers) are registered there.

## API

- `POST /api-token-auth/` with `username`/`password` returns a token.
- `/api/managers/` — list, retrieve, create, update, and delete manager accounts of the authenticated owner (token or session auth, `Authorization: Token <token>`).

## Linting

```sh
flake8
isort --check .
```

## Author

- https://github.com/biloskurskyi
- https://www.linkedin.com/in/valerii-biloskurskyi-175429281/
