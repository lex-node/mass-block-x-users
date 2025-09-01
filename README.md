# mass-block-x-users

Mass block a list of X users.

## Installation

1. Clone the repository and change into it:

   ```bash
   git clone <repo-url>
   cd mass-block-x-users
   ```

2. (Optional) Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Windows

Use the following commands in PowerShell to set up the project on Windows:

```powershell
git clone <repo-url>
cd mass-block-x-users
py -3 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Running the web application

1. Set the Flask entry point:

   ```bash
   export FLASK_APP=web_app.py
   ```

2. Start the development server:

   ```bash
   flask run
   ```

   The app will be available at http://localhost:5000/.

3. In your browser, upload a text file containing one username per line and
   provide the required `source_id` and `token`. Submit the form to block the
   listed users. A results page will display the status for each user.

   You can also run the app directly with Python:

   ```bash
   python web_app.py
   ```

### Windows

On Windows, configure and run the application with:

```powershell
set FLASK_APP=web_app.py
flask run
```

The app will be available at http://localhost:5000/.

You can also run the app directly with:

```powershell
python web_app.py
```

## Tests

Run the unit tests with:

```bash
pytest
```

## Docker

Build and run the container:

```bash
docker build -t mass-block-x-users .
docker run --rm -p 5000:5000 mass-block-x-users
```

The application is exposed on port 5000.

