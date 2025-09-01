# mass-block-x-users

Mass block a list of X users.

VIBE-CODED APP, EXPERIMENTAL, UNAUDITED, NON-SECURE, NO REPRESENTATIONS/WARRANTIES GIVEN, AS-IS/WHERE-IS, USE AT YOUR OWN RISK 

## Getting started (no experience required)

Follow these steps to install and run the app on your computer. All commands assume
you have installed the Python dependencies with `pip install -r requirements.txt`.

### 1. Install prerequisites

- **Git** – download from https://git-scm.com/downloads and install it.
- **Python 3** – download from https://www.python.org/downloads/ and install.

### 2. Clone this repository

Open a terminal (macOS/Linux) or PowerShell (Windows) and run:

```bash
git clone https://github.com/<your-username>/mass-block-x-users.git
cd mass-block-x-users
```

Replace the URL with the address of this repository if it is different.

### 3. Start the app using the helper script

The repository includes scripts that set up a virtual environment, install the dependencies and launch the web server.

#### macOS or Linux

```bash
./start.sh
```

If you get a "permission denied" error, run `chmod +x start.sh` once and try again.

#### Windows

```powershell
.\start.ps1
```

If PowerShell blocks the script, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\start.ps1
```

The server will start on http://localhost:5000/.

### 4. Use the app

In your browser visit http://localhost:5000/.
Upload a text file with one username per line and enter your `source_id`, `token`, `ct0`, and `bearer_token` from X. Submit the form to block each user and review the results.

You can alternatively set the `SOURCE_ID`, `AUTH_TOKEN`, `CT0`, and `BEARER_TOKEN` environment variables before launching the app and leave the fields blank in the form.

#### Finding your `source_id`, `token`, `ct0`, and `bearer_token`

These pieces of information tell X which account is doing the blocking and authorize the requests.

- **source_id** – This is your numeric X user ID. To find it, visit <https://x.com/settings/your_twitter_data> and look for **User ID** in the *Account* section, or use <https://get-id-x.foundtt.com/en/> to look it up.
- **token** – This is the `auth_token` cookie from your browser. With X open in your browser:
  1. Press <kbd>F12</kbd> to open the developer tools.
  2. Go to the **Application** (or **Storage**) tab and open the **Cookies** entry for `https://x.com`.
  3. Find the cookie named `auth_token` and copy its value.
- **ct0** – Another cookie found alongside `auth_token`. Copy the value of the `ct0` cookie from the same list.
- **bearer_token** – Inspect any network request on X in the **Network** tab and copy the value from the `Authorization: Bearer` header.

Keep these tokens secret; anyone with them can act on your X account.

The home page also links to **Block SOL Shills**, which blocks a predefined set of usernames without uploading a file.

## Manual setup (optional)

If you prefer to set up the environment yourself:

1. **Create and activate a virtual environment**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate       # macOS/Linux
   ```

   ```powershell
   py -3 -m venv .venv
   .\.venv\Scripts\activate        # Windows
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**

   ```bash
   export FLASK_APP=web_app.py     # macOS/Linux
   flask run
   ```

   ```powershell
   set FLASK_APP=web_app.py        # Windows
   flask run
   ```

## Tests

Run the unit tests with:

```bash
pytest
```

Install required packages first with:

```bash
pip install -r requirements.txt
```

## Docker

Build and run the container:

```bash
docker build -t mass-block-x-users .
docker run --rm -p 5000:5000 mass-block-x-users
```

The application is exposed on port 5000.
