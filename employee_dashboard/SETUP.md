# Employee Dashboard - Repository and Local Setup

This guide covers creating your own GitHub repository, sharing it with teammates, and installing a local copy on Windows. Cloning the repository downloads the code; it does not publish the dashboard or create a shared internet URL.

## What you need

- Windows 10 or 11.
- Python 3.10 or newer. During installation, enable the Python launcher (`py`) if the installer offers it.
- Git for Windows.
- A GitHub account and permission to create a repository.
- Internet access to clone the repository and install the Python packages.

## 1. Create your private GitHub repository

On GitHub, create a **Private** repository. For the first push, leave the options to create a README, `.gitignore`, or license unchecked; this project already has these files.

There are two folders to note:

- **Repository root:** the folder that contains `.git` and where `git clone` creates the repository.
- **Project folder:** the `employee_dashboard` folder inside the repository, containing this setup guide and `requirements.txt`.

Run Git commands from the repository root. In the current layout, enter the outer `employee_dashboard` folder containing the inner `employee_dashboard` folder. If this folder is not already a Git repository of its own, initialize it:

```powershell
git init -b main
```

Before staging, confirm that the real workbook and local credentials are ignored:

```powershell
git check-ignore employee_dashboard\Employee_data.xlsx employee_dashboard\.env employee_dashboard\data\data.py
git status --short
```

`git check-ignore` should list all three paths. If it does not, stop and check `employee_dashboard\.gitignore`. Never commit the real employee workbook, `.env`, password hashes, session secrets, or the SharePoint URL. The workbook is read directly from the authorized SharePoint link.

If you have not configured Git on this computer before, set your commit identity:

```powershell
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Stage, review, commit, and push the project code. First create the repository on GitHub, open it, and copy the **HTTPS** URL from its **Code** button. This is a Git command, not a dashboard login link. Replace the example URL below with the URL you copied; do not use the literal placeholder names.

```powershell
git add .
git status
git diff --cached --stat
git commit -m "Initial employee dashboard"
git remote add origin https://github.com/ACTUAL_USERNAME/ACTUAL_REPOSITORY.git
git push -u origin main
```

Review the staged changes before committing. If `git remote add origin` says that `origin` already exists, replace it with your real repository URL and push:

```powershell
git remote set-url origin https://github.com/ACTUAL_USERNAME/ACTUAL_REPOSITORY.git
git remote -v
git push -u origin main
```

If pushing returns **404**, verify that the repository exists and the URL matches its GitHub HTTPS URL exactly. For a private repository, make sure you are authenticated to GitHub with an account that has access.

## 2. Teammates clone the repository

Invite teammates as collaborators to the private GitHub repository. They need Git installed and permission to access it. In PowerShell, each teammate clones the repo and changes into the inner project folder:

```powershell
cd C:\path\where\you\keep\projects
git clone https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME.git
cd YOUR_REPOSITORY_NAME
cd employee_dashboard
```

Replace the example path and repository URL with the values for your team. Run the Python setup and app commands below from this inner project folder. Each teammate configures `EXCEL_PATH` to their synced workbook; do not send `.env` or the workbook to unauthorized users.

## 3. Check Python

```powershell
py -3 --version
```

The version must be Python 3.10 or newer. If `py` is not recognized, install Python from the official Python distribution and reopen PowerShell.

## 4. Create a virtual environment and install packages

```powershell
py -3 -m venv venv
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

The virtual environment keeps this project's packages separate from other Python projects.

## 5. Configure the workbook URL and create your local login

```powershell
.\venv\Scripts\python.exe setup_login.py
```

Enter an email address and a password of at least 12 characters when prompted, then confirm the password. The setup script creates a `.env` file in the project root containing the email, salted password hash, and session-signing secret. It does not store the plain-text password. Keep `.env` private; it is excluded from Git and should not be sent to teammates.

Each local installation needs its own `.env` and login. If `.env` already exists, the setup script will not overwrite it.

The dashboard reads only the `Data Practice Resources` worksheet from a local workbook. Set `EXCEL_PATH` in `.env` to the workbook in your OneDrive/SharePoint-synced folder:

```text
EXCEL_PATH="C:\\Users\\YourName\\OneDrive - YourOrganization\\Data Practice Resources.xlsx"
```

Replace the example with the actual synced file path. The default path is `Employee_data.xlsx` in the project folder if `EXCEL_PATH` is not set. The backend only reads the file and never writes to it. Do not commit the workbook or the local `data\data.py` file containing the SharePoint link.

## 6. Start the dashboard

```powershell
.\run.bat
```

Keep the PowerShell window open while using the dashboard. To stop the server, focus that window and press **Ctrl+C**.
After pulling project code updates, stop the server with **Ctrl+C**, start it again with `.\run.bat`, and reload the browser page.

## 7. Sign in

On the same computer, open:

**http://localhost:8000/login**

Sign in with the email and password created in step 5. Use **Sign out** to end the session.

## 8. Refresh workbook data

The server checks the synced workbook for changes every 10 seconds and reloads the displayed data when it changes. **Refresh data** is also available for immediate manual refresh. The server must have read access to the configured path.

The workbook must contain a worksheet named `Data Practice Resources` with these exact headers in the first row:

| # | Employee ID | Employee Name | Technical Skills | YOE | Email | DOJ DEP | Internal/External | Mapped to Project | Billable from | Client Name | Certification Name | Date of Completion | Expected Date of Completion | Profiles Uploaded | Contact Number |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

Other sheets and columns are ignored. The dashboard does not write or update workbook data.

## Important: local copy versus team-wide access

These steps run the app on the teammate's own computer at `localhost`. Each installation reads the workbook at its configured local sync path. The app sees changes after OneDrive or SharePoint sync updates that local file.

The launcher listens on the computer's network interfaces, but that does not make the app available over the internet. Do not expose this development server or its port directly to the public internet. To provide one shared dashboard, deploy it to an approved Python hosting service with HTTPS and provision the workbook at a readable `EXCEL_PATH` on that host. A local OneDrive sync path is not automatically available to a hosted service.

## Publish a free demo on Render

The repository root contains `render.yaml` for a public demo deployment. It uses the synthetic `data/employees.xlsx`, not the private `Employee_data.xlsx`.

1. Push the repository to GitHub, then sign in to Render and choose **New → Blueprint**.
2. Connect the GitHub repository and deploy the `employee-dashboard-demo` service from `render.yaml`.
3. When prompted for `LOGIN_EMAIL` and `LOGIN_PASSWORD_HASH`, provide the demo account email and the hash from your local `.env`. Do not paste or upload the `.env` file; Render generates its own `SESSION_SECRET`.
4. After Render reports the service is live, open its `onrender.com` URL with `/login` appended and share that HTTPS URL with your team. Do not share `http://localhost:8000/`; that points to each teammate's own computer.

The free service may take a short time to wake after inactivity. It is a synthetic demo only and does not use or expose the private SharePoint workbook. To publish the real dashboard, use an approved host, configure the authorized SharePoint URL in protected environment settings, and keep the sharing URL and login credentials out of Git.

## Troubleshooting

| Problem | What to do |
|---|---|
| `py` is not recognized | Install Python 3.10+ with the Python launcher, then reopen PowerShell. |
| `No module named ...` | From the project root, run `.\venv\Scripts\python.exe -m pip install -r requirements.txt`. |
| `setup_login.py` says `.env` already exists | Keep using the account already configured, or have the account owner securely manage the local `.env`. Do not delete it unless you intend to configure a new local login. |
| Server reports missing authentication settings | Run step 5 to configure the local login, then restart the server. |
| Workbook file not found | Check that `EXCEL_PATH` points to the synced workbook and that the server can read it. |
| 500 Missing columns | Check the exact headers on the `Data Practice Resources` worksheet. |
| Teammate cannot open `localhost` link | `localhost` refers to the computer opening the link. Deploy the app and share the host's HTTPS URL instead. |
| Port 8000 is already in use | Stop the other app using port 8000, or have the project owner update the port consistently in `run.bat` and the URL. |
| Styling is missing | The page needs internet access to load Bootstrap from its CDN. |
