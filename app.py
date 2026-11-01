import os
import uuid

from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# قائمة المهام في الذاكرة (للتبسيط)
todos = []

@app.route('/')
def index():
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    task = request.form.get('task')
    if task:
        todos.append({
            'id': str(uuid.uuid4()),
            'task': task,
            'completed': False
        })
    return redirect(url_for('index'))

@app.route('/complete/<todo_id>', methods=['POST'])
def complete_todo(todo_id):
    for todo in todos:
        if todo['id'] == todo_id:
            todo['completed'] = not todo['completed']
            break
    return redirect(url_for('index'))

@app.route('/delete/<todo_id>', methods=['POST'])
def delete_todo(todo_id):
    global todos
    todos = [todo for todo in todos if todo['id'] != todo_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Debug mode and network exposure are opt-in: the Werkzeug debugger must not
    # be reachable from other machines. Use FLASK_DEBUG=1 / FLASK_HOST=0.0.0.0
    # only on a trusted local network.
    app.run(
        debug=os.environ.get('FLASK_DEBUG') == '1',
        host=os.environ.get('FLASK_HOST', '127.0.0.1'),
        port=int(os.environ.get('PORT', '5000')),
    )
