# Employee Dashboard

Internal dashboard built from an Excel file: **Excel -> Pandas -> FastAPI -> HTML/Bootstrap/Chart.js**. The dashboard requires an email and password to sign in.
The dashboard reads `Employee_data.xlsx` from the project root. The real workbook is excluded from Git because it contains employee information; distribute it only through approved secure sharing. Dashboard pages check for workbook changes every 10 seconds and automatically reload the displayed data after the workbook is saved. **Refresh data** is also available for immediate manual refresh.

## Folder structure

```
employee_dashboard/
├── backend/
│   ├── main.py                  App entry point (API + serves frontend)
│   ├── auth_utils.py            Password hashing and verification
│   ├── config.py                Excel path and column mapping
│   ├── schemas.py               Pydantic response models
│   ├── routers/                 auth.py, dashboard.py, employees.py
│   └── services/                excel_service.py, dashboard_service.py
├── Employee_data.xlsx           Local source data (ignored by Git; distribute securely)
├── setup_login.py               Securely configure the dashboard login
├── frontend/
│   ├── index.html, employees.html
│   ├── css/style.css
│   └── js/                      common.js, dashboard.js, employees.js
├── data/employees.xlsx          Optional sample data (not used by the dashboard)
├── tests/test_api.py
├── generate_sample_data.py      Creates sample Excel data
├── requirements.txt
├── run.bat / run.sh             Start the server
└── README.md
```

## Setup

For steps to create your own private GitHub repository, share it with teammates to clone, and install/run local copies on Windows, see [SETUP.md](./SETUP.md). Requires Git for Windows and Python 3.10+.

## Configure login

From the project root, run:

```
python setup_login.py
```

Enter the one dashboard account email and a password of at least 12 characters. The script stores a salted password hash and a random session-signing secret in `.env`; it does not save the plain-text password. `.env` is ignored by Git. Do not share or commit it. The setup script refuses to overwrite an existing `.env`.

For local HTTP testing, the generated configuration uses `COOKIE_SECURE=false`. **Before hosting on the internet, set `COOKIE_SECURE=true` and serve the app only over HTTPS.** Keep the session secret and password hash in the hosting provider's protected environment settings; do not upload `.env` or put credentials in source code.

## Run

On Windows, run `run.bat` from this project folder. On macOS/Linux, run `./run.sh`. These launchers listen on `0.0.0.0:8000`. Keep the terminal and host computer running.

- On the host computer: http://localhost:8000
- The sign-in page is shown before the dashboard and employee API are available.

Running on your PC does not create a public internet URL. `http://localhost:8000/` works only on the computer running the app. For a public demo, this repository includes a Render Blueprint in the repository root; it serves the synthetic `data/employees.xlsx` and uses HTTPS. See [SETUP.md](./SETUP.md) for deployment steps. The free Render service is not suitable for the private, manager-edited workbook because its filesystem is not persistent. For the real dashboard, use an approved host and persistent or securely integrated workbook storage. Do not expose the development server directly to the public internet.

The configured login is a single shared account for this initial version; it does not provide individual user accounts or account recovery. Share the credentials only with authorized teammates.

## Excel rules

`Employee_data.xlsx` is ignored by Git because it contains employee information. Place the authorized workbook in the project root using an approved secure sharing method. It must have these headers in row 1 (exact names):

| S.no | Employee ID | Employee Name | Managers | Email | Mapped to Project | Location | Contact Number |
|---|---|---|---|---|---|---|

- One row per employee, no merged cells. Blank cell values appear as empty values in the dashboard.
- The manager filter and manager employee counts use the `Managers` column. Saved changes to manager names or assignments appear automatically.
- The API checks the workbook file's modification time, change time, and size, so saved additions, edits, and deletions are detected. If Excel temporarily locks the workbook during a save, refresh retries automatically.
- Set optional `EXCEL_PATH` in `.env` to an absolute path or a path relative to the project root if the workbook is stored elsewhere. The server must be able to read that file.
- Automatic refresh works when the running server can read the manager's saved workbook at the configured `EXCEL_PATH`. If the manager edits a separate copy on another computer, use a shared/synced workbook path accessible to the server or an upload/integration workflow; the app cannot detect edits to a different file.
- After pulling code updates that change the backend, stop the running server with `Ctrl+C`, start it again, and reload the browser page.
- `python generate_sample_data.py` creates a separate sample workbook at `data/employees.xlsx` and does not overwrite the dashboard source.

## API

| Endpoint | Description |
|---|---|
| POST /api/auth/login | Sign in and create a secure session |
| POST /api/auth/logout | End the current session |
| GET /api/dashboard/version | Version marker used to detect workbook changes |
| GET /api/dashboard/summary | Totals for the four cards |
| GET /api/dashboard/by-location | Employee count per location |
| GET /api/dashboard/by-manager | Employee count per manager |
| GET /api/dashboard/project-mapping | Counts by “Mapped to Project” value |
| GET /api/employees?manager=&location=&mapped_to_project= | All employee columns, with optional filters |

## Tests

```
pytest
```

## Troubleshooting

| Problem | Fix |
|---|---|
| Missing authentication settings | Run `python setup_login.py` and restart the server |
| Login cookie is not retained on the internet host | Use HTTPS and set `COOKIE_SECURE=true` |
| No module named 'backend' | Run commands from the project root |
| 503 Excel file not found | Ensure `Employee_data.xlsx` is in the project root |
| 500 Missing columns | Header names in row 1 must match exactly |
| No styling or chart | The CDN is blocked; download Bootstrap and Chart.js locally |
| Others cannot connect | Confirm deployment/network routing and firewall settings; use HTTPS for internet access |
