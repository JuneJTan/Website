# Backend Usage

This project now uses Django for the website backend and admin editing.

## Run Locally

```powershell
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

Open:

- Front page: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`

## Create Admin User

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

After logging into `/admin/`, the editable modules are:

- Site profile
- Research areas
- People
- Publications
- Courses
- News items
- Positions

## Uploaded Files

Files uploaded from the admin are stored under:

```text
media/
```

Uploaded images and PDFs are served by Django during local development.

## Re-import Legacy Publications

The old website publication lists were imported from:

```text
legacy_reference/extracted_publications/publications.json
```

To re-import and replace all current publication records:

```powershell
.\.venv\Scripts\python.exe manage.py import_publications --clear
```

Current imported publication counts:

- Journal papers: 110
- Books and book chapters: 4
- Conference proceedings: 135
- Workshop and invited seminar presentations: 35

## Verification Commands

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py showmigrations cms
```
