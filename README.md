# Cloud-Based Bus Pass System

A beginner-friendly Flask demo for submitting bus pass applications and reviewing their status.

## Features
- Application form with name, email, phone, route, pass type and start date
- Basic validation and dashboard counters
- Change request status to Pending, Approved or Rejected
- Health endpoint at `/health`
- Parameterized SQL queries and responsive layout

## Run on Windows / VS Code
1. Extract this ZIP and open the project folder in VS Code.
2. Open Terminal → New Terminal.
3. Create an environment: `py -m venv .venv`
4. Install dependencies: `.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt`
5. Run: `.\\.venv\\Scripts\\python.exe app.py`
6. Visit `http://127.0.0.1:5000`. Health check: `http://127.0.0.1:5000/health`.

If `py` is not recognized, use `python` instead.

## Tests
Run `.\\.venv\\Scripts\\python.exe -m pytest -q` after installing dependencies.
Manually test a valid application, invalid email, status update and `/health`.

## Push to GitHub
Create an empty GitHub repository, e.g. `CodeAlpha_Cloud_Bus_Pass_System`. Run these commands from the project folder:
```powershell
git init
git add .
git commit -m "Build cloud-based bus pass system"
git branch -M main
git remote add origin https://github.com/YOUR-GITHUB-USERNAME/CodeAlpha_Cloud_Bus_Pass_System.git
git push -u origin main
```
Replace `YOUR-GITHUB-USERNAME`. Never commit secrets, `.env`, the virtual environment or the generated database.

## Cloud deployment note
The included Procfile uses Gunicorn. SQLite files may be temporary on some cloud platforms; for a reliable public deployment, use a managed persistent database such as PostgreSQL and add administrator authentication first.

## Project scope
This is an educational demo. It does not include user login, payments, QR pass generation or official bus operator integration. Status updates are not protected by administrator authentication.
