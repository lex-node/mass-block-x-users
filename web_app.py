from flask import Flask, request, render_template_string, url_for, jsonify
from block import block_from_file, SOL_SHILLS
import os
import threading
import uuid
from dataclasses import dataclass, field
from typing import Dict, Optional

app = Flask(__name__)

@dataclass
class Task:
    """Simple structure to track background task state."""

    status: str = "pending"
    progress: Dict[str, int] = field(
        default_factory=lambda: {"current": 0, "total": 0}
    )
    result: Optional[Dict[str, str]] = None


# In-memory task tracking
tasks: Dict[str, Task] = {}
tasks_lock = threading.Lock()

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

TASK_TEMPLATE = """
<!doctype html>
<title>Task Submitted</title>
<h1>Task Submitted</h1>
<p>Task ID: {{ task_id }}</p>
<p>Check <a href="{{ status_url }}">task status</a>.</p>
<a href="{{ url_for('index') }}">Back</a>
"""


def _block_sol_shills_task(
    task_id: str,
    source_id: str,
    token: str,
    ct0: str,
    bearer_token: str,
) -> None:
    """Background worker to block SOL shills."""

    app.logger.info("Task %s started", task_id)
    total = len(SOL_SHILLS)
    results: dict[str, str] = {}
    with tasks_lock:
        task = tasks[task_id]
        task.status = "running"
        task.progress = {"current": 0, "total": total}
    for idx, username in enumerate(SOL_SHILLS, start=1):
        partial = block_from_file(
            [username],
            source_id,
            token,
            ct0=ct0,
            bearer_token=bearer_token,
        )
        results.update(partial)
        with tasks_lock:
            tasks[task_id].progress = {"current": idx, "total": total}
        app.logger.info("Task %s progress: %s/%s", task_id, idx, total)
    with tasks_lock:
        task = tasks[task_id]
        task.status = "finished"
        task.result = results
    app.logger.info("Task %s finished", task_id)


@app.route('/block-sol-shills', methods=['GET', 'POST'])
def block_sol_shills_route():
    if request.method == 'POST':
        source_id = request.form.get('source_id') or os.getenv('SOURCE_ID', '')
        token = request.form.get('token') or os.getenv('AUTH_TOKEN', '')
        ct0 = request.form.get('ct0') or os.getenv('CT0', '')
        bearer_token = request.form.get('bearer_token') or os.getenv('BEARER_TOKEN', '')
        task_id = str(uuid.uuid4())
        with tasks_lock:
            tasks[task_id] = Task()
        app.logger.info("Scheduling task %s to block SOL shills", task_id)
        thread = threading.Thread(
            target=_block_sol_shills_task,
            args=(task_id, source_id, token, ct0, bearer_token),
            daemon=True,
        )
        thread.start()
        status_url = url_for('task_status', task_id=task_id, _external=True)
        return render_template_string(
            TASK_TEMPLATE, task_id=task_id, status_url=status_url
        )
    return render_template_string(SOL_SHILLS_TEMPLATE)


@app.route('/tasks/<task_id>')
def task_status(task_id: str):
    with tasks_lock:
        task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "task not found"}), 404
    if task.status == "finished":
        return jsonify(
            {
                "status": task.status,
                "progress": task.progress,
                "result": task.result,
            }
        )
    return jsonify({"status": task.status, "progress": task.progress})


if __name__ == '__main__':
    app.run()
