from flask import Flask, request, render_template_string
from block import block_from_file

app = Flask(__name__)

FORM_TEMPLATE = """
<!doctype html>
<title>Mass Block X Users</title>
<h1>Upload user list</h1>
<form method="post" enctype="multipart/form-data">
  <label>Username file: <input type="file" name="userfile" required></label><br>
  <label>Source ID: <input type="text" name="source_id" required></label><br>
  <label>Token: <input type="password" name="token" required></label><br>
  <input type="submit" value="Block">
</form>
"""

RESULT_TEMPLATE = """
<!doctype html>
<title>Block Results</title>
<h1>Block Results</h1>
<ul>
  {% for user, status in results.items() %}
    <li>{{ user }}: {{ status }}</li>
  {% endfor %}
</ul>
<a href="{{ url_for('index') }}">Back</a>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded = request.files.get('userfile')
        source_id = request.form.get('source_id', '')
        token = request.form.get('token', '')
        if not uploaded:
            return "No file uploaded", 400
        results = block_from_file(uploaded.stream, source_id, token)
        return render_template_string(RESULT_TEMPLATE, results=results)
    return render_template_string(FORM_TEMPLATE)


if __name__ == '__main__':
    app.run()
