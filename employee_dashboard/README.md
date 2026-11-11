# Employee Dashboard

Internal dashboard built from an Excel file: **Excel -> Pandas -> FastAPI -> HTML/Bootstrap**. The dashboard requires an email and password to sign in.
The dashboard reads only the `Data Practice Resources` worksheet from the configured local workbook path. Set `EXCEL_PATH` to the workbook in a OneDrive/SharePoint-synced folder. Dashboard pages check for workbook changes every 10 seconds and automatically reload the displayed data after it is saved. **Refresh data** is also available for immediate manual refresh.

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
├── setup_login.py               Securely configure the dashboard login
├── frontend/
│   ├── index.html, employees.html
│   ├── css/style.css
│   └── js/                      common.js, dashboard.js, employees.js
├── data/employees.xlsx          Synthetic demo workbook (generated for Render)
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

Running on your PC does not create a public internet URL. `http://localhost:8000/` works only on the computer running the app. For a public demo, this repository includes a Render Blueprint in the repository root; the build generates a synthetic `data/employees.xlsx` with the expected worksheet and uses HTTPS. See [SETUP.md](./SETUP.md) for deployment steps. The demo does not use or expose the private SharePoint workbook. For the real dashboard, use an approved host and keep the sharing URL private. Do not expose the development server directly to the public internet.

The configured login is a single shared account for this initial version; it does not provide individual user accounts or account recovery. Share the credentials only with authorized teammates.

## Excel rules

The app reads the workbook at `EXCEL_PATH`; point this setting to a local OneDrive/SharePoint-synced copy or place `Employee_data.xlsx` in the project folder. The app does not write or update workbook data.

The `Data Practice Resources` worksheet must contain these exact headers in its first row. Other worksheets and columns are ignored:

| # | Employee ID | Employee Name | Technical Skills | YOE | Email | DOJ DEP | Internal/External | Mapped to Project | Billable from | Client Name | Certification Name | Date of Completion | Expected Date of Completion | Profiles Uploaded | Contact Number |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

- Keep the worksheet to one employee per row. Blank cell values appear as empty values in the dashboard.
- Dashboard refresh checks the workbook version every 10 seconds using its file modification time, change time, and size.
- Set `EXCEL_PATH` in `.env` to an absolute path or a path relative to the project root.
- After pulling code updates that change the backend, stop the running server with `Ctrl+C`, start it again, and reload the browser page.
- `python generate_sample_data.py` creates the synthetic `data/employees.xlsx` workbook used by the public demo only.

## API

| Endpoint | Description |
|---|---|
| POST /api/auth/login | Sign in and create a secure session |
| POST /api/auth/logout | End the current session |
| GET /api/dashboard/version | Version marker used to detect workbook changes |
| GET /api/dashboard/summary | Employee, mapping, internal and external totals |
| GET /api/dashboard/project-mapping | Counts by non-empty “Mapped to Project” value |
| GET /api/employees?internal_external=&mapped_to_project= | Supplied employee columns, with optional filters |

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
| 503 Excel file not found | Check that `EXCEL_PATH` points to the synced workbook and that the server can read it |
| 500 Missing columns | Check the exact headers on the `Data Practice Resources` worksheet |
| No styling | The CDN is blocked; download Bootstrap locally |
| Others cannot connect | Confirm deployment/network routing and firewall settings; use HTTPS for internet access |
