# mass-block-x-users

Mass block a list of X users.

## Web application

A simple Flask app provides a form to upload a list of usernames along with a
`source_id` and `token`. On submission it calls `block_from_file` and displays
the result for each user.

### Run with Flask

```bash
pip install -r requirements.txt
export FLASK_APP=web_app.py
flask run
```

The application will be available at http://localhost:5000/

### Tests

Run the unit tests with:

```bash
pytest
```

### Docker

```bash
docker build -t mass-block-x-users .
docker run -p 5000:5000 mass-block-x-users
```

The container exposes the app on port 5000.
