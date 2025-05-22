# Django REST API

## Start postgres
docker compose up -d

## Start API
### With uv
- uv sync
- uv run test_task/manage.py migrate
- uv run test_task/manage.py runserver
### With python
- python -m venv venv
- venv/scripts/activate
- pip install -r requirements.txt
- python test_task/manage.py migrate
- python test_task/manage.py runserver

## Requirements
Requires OSGeo4W to run

### .env example
DB_NAME=

DB_USER=

DB_PASSWORD=

DB_HOST=

DB_PORT=


