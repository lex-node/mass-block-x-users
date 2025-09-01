# PowerShell script to set up a virtual environment, install dependencies, and start the Flask app.
# Run this from PowerShell on Windows.

if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
    Write-Error "Python 3 is required. Download it from https://www.python.org/downloads/"
    exit 1
}

if (-not (Test-Path '.venv')) {
    py -3 -m venv .venv
}

& .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:FLASK_APP = 'web_app.py'
flask run
