from flask import Flask, request, render_template_string
from block import block_from_file, block_sol_shills
import os

app = Flask(__name__)

FORM_TEMPLATE = """
<!doctype html>
<title>Mass Block X Users</title>
<h1>Upload user list</h1>
<form method="post" enctype="multipart/form-data">
  <label>Username file: <input type="file" name="userfile" required></label><br>
  <label>Source ID: <input type="text" name="source_id"></label><br>
  <label>Token: <input type="password" name="token"></label><br>
  <label>ct0: <input type="text" name="ct0"></label><br>
  <label>Bearer Token: <input type="password" name="bearer_token"></label><br>
  <input type="submit" value="Block">
</form>
<p>Or <a href="{{ url_for('block_sol_shills_route') }}">Block SOL Shills</a></p>
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
        source_id = request.form.get('source_id') or os.getenv('SOURCE_ID', '')
        token = request.form.get('token') or os.getenv('AUTH_TOKEN', '')
        ct0 = request.form.get('ct0') or os.getenv('CT0', '')
        bearer_token = request.form.get('bearer_token') or os.getenv('BEARER_TOKEN', '')
        if not uploaded:
            return "No file uploaded", 400
        results = block_from_file(
            uploaded.stream,
            source_id,
            token,
            ct0=ct0,
            bearer_token=bearer_token,
        )
        return render_template_string(RESULT_TEMPLATE, results=results)
    return render_template_string(FORM_TEMPLATE)


SOL_SHILLS_TEMPLATE = """
<!doctype html>
<title>Block SOL Shills</title>
<h1>Block SOL Shills</h1>
<form method="post">
  <label>Source ID: <input type="text" name="source_id"></label><br>
  <label>Token: <input type="password" name="token"></label><br>
  <label>ct0: <input type="text" name="ct0"></label><br>
  <label>Bearer Token: <input type="password" name="bearer_token"></label><br>
  <input type="submit" value="Block SOL Shills">
</form>
"""


@app.route('/block-sol-shills', methods=['GET', 'POST'])
def block_sol_shills_route():
    if request.method == 'POST':
        source_id = request.form.get('source_id') or os.getenv('SOURCE_ID', '')
        token = request.form.get('token') or os.getenv('AUTH_TOKEN', '')
        ct0 = request.form.get('ct0') or os.getenv('CT0', '')
        bearer_token = request.form.get('bearer_token') or os.getenv('BEARER_TOKEN', '')
        results = block_sol_shills(
            source_id,
            token,
            ct0=ct0,
            bearer_token=bearer_token,
        )
        return render_template_string(RESULT_TEMPLATE, results=results)
    return render_template_string(SOL_SHILLS_TEMPLATE)


if __name__ == '__main__':
    app.run()
