# kubehub-backend

## Requirements

- python3.7
- django 3.0.2

## Developing

### Setup virtualenv

Create and setup virtualenv:
```
python3.7 -m venv env
```
or
```
virtualenv --python=/usr/bin/python3.7 venv
```

### Project setup

Install required libs:
```
pip install -r requirements.txt
```

### Run project
```
python manage.py runserver
```

#### Examples of curl request for CRUD api

List of cloud providers request to `/api/cloud_providers/list`:

```
curl --request GET http://localhost:8000/api/cloud_providers/list
```

Add cloud provider request to `/api/cloud_providers/add`:
```
curl -d '{"cp_type": "value1", "name": "value2", "api_endpoint": "value3", "password": "value4"}' -H "Content-Type: application/json" -X POST http://localhost:8000/api/cloud_providers/add
```

Edit cloud provider request to `/api/cloud_providers/edit`:
```
curl -d '{"field_to_edit1": "value1", ..., "field_to_edit_n": "valuen"}' -H "Content-Type: application/json" -X POST http://localhost:8000/api/cloud_providers/edit
```

Remove cloud provider request to `/api/cloud_providers/remove`:
```
curl -d '{"id": "value"}' -H "Content-Type: application/json" -X POST http://localhost:8000/api/cloud_providers/remove
```