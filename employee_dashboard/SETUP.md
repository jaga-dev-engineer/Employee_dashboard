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
git check-ignore employee_dashboard\Employee_data.xlsx employee_dashboard\.env
git status --short
```

`git check-ignore` should list both files. If it does not, stop and check `employee_dashboard\.gitignore`. Never commit the real employee workbook, `.env`, password hashes, or session secrets. `Employee_data.xlsx` is excluded from Git because it contains employee information; provide it to authorized teammates separately using your organization's approved secure file sharing.

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

Replace the example path and repository URL with the values for your team. Run the Python setup and app commands below from this inner project folder. Teammates must get `Employee_data.xlsx` separately from the approved secure file-sharing location and copy it into this folder beside `requirements.txt`. Do not send `.env`; each teammate creates their own local login in step 5.

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

## 5. Copy the workbook and create your local login

Copy the authorized `Employee_data.xlsx` into the project root. It belongs beside `README.md` and `requirements.txt` and is deliberately not included in the Git repository.

```powershell
.\venv\Scripts\python.exe setup_login.py
```

Enter an email address and a password of at least 12 characters when prompted, then confirm the password. The setup script creates a `.env` file in the project root containing the email, salted password hash, and session-signing secret. It does not store the plain-text password. Keep `.env` private; it is excluded from Git and should not be sent to teammates.

Each local installation needs its own `.env` and login. If `.env` already exists, the setup script will not overwrite it.

## 6. Start the dashboard

```powershell
.\run.bat
```

Keep the PowerShell window open while using the dashboard. To stop the server, focus that window and press **Ctrl+C**.

## 7. Sign in

On the same computer, open:

**http://localhost:8000/login**

Sign in with the email and password created in step 5. Use **Sign out** to end the session.

## 8. Refresh workbook data

Edit `Employee_data.xlsx` in the project root and save the workbook. Click **Refresh data** on the dashboard or reload the page. The dashboard also checks for saved changes every 60 seconds. Do not edit the workbook while it is open in Excel if Excel prevents other programs from reading the saved file.

The workbook must have these exact headers in the first row:

| S.no | Employee ID | Employee Name | Email | Mapped to Project | Location | Contact Number |
|---|---|---|---|---|---|---|

## Important: local copy versus team-wide access

These steps run the app on the teammate's own computer at `localhost`. Each person has their own copy of the workbook, so changes made to one person's file do not automatically appear on other people's computers.

The launcher listens on the computer's network interfaces, but that does not make the app available over the internet. Do not expose this development server or its port directly to the public internet. To provide one shared live dashboard, deploy it to an approved Python hosting service with HTTPS, configure the login settings securely on that host, and store the workbook in the deployed app's persistent storage.

## Troubleshooting

| Problem | What to do |
|---|---|
| `py` is not recognized | Install Python 3.10+ with the Python launcher, then reopen PowerShell. |
| `No module named ...` | From the project root, run `.\venv\Scripts\python.exe -m pip install -r requirements.txt`. |
| `setup_login.py` says `.env` already exists | Keep using the account already configured, or have the account owner securely manage the local `.env`. Do not delete it unless you intend to configure a new local login. |
| Server reports missing authentication settings | Run step 5 to configure the local login, then restart the server. |
| `Employee_data.xlsx` not found | Obtain the workbook through your approved secure sharing method and put it in the project root beside `requirements.txt`. |
| Port 8000 is already in use | Stop the other app using port 8000, or have the project owner update the port consistently in `run.bat` and the URL. |
| Styling or chart is missing | The page needs internet access to load Bootstrap and Chart.js from their CDN. |
