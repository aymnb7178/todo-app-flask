# Todo App (Flask)

A small task-management web app built with Flask and Tailwind CSS, with an Arabic right-to-left interface. It is a working prototype: tasks are kept in memory and are lost when the server restarts.

> النسخة العربية: [README.ar.md](README.ar.md)

## Overview

Add tasks, mark them complete, and delete them from a single page. The page also shows counters for total, completed, and remaining tasks.

## Key Features

- Add a new task
- Toggle a task as completed / not completed
- Delete a task (with a confirmation prompt)
- Task counters (total / completed / remaining)
- Arabic RTL layout using Tailwind CSS (via CDN) and Noto Sans Arabic

## Technologies Used

- Python 3, Flask
- Jinja2 templates
- HTML5, Tailwind CSS (CDN), JavaScript
- gunicorn (listed in `requirements.txt` for deployment)

## Project Structure

```
todo-app-flask/
├── app.py              # Flask application and routes
├── requirements.txt    # Python dependencies
└── templates/
    └── index.html      # Single-page Arabic RTL interface
```

## Installation

```bash
git clone https://github.com/aymnb7178/todo-app-flask.git
cd todo-app-flask
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## How to Run

```bash
python app.py
```

Then open http://127.0.0.1:5000 in your browser.

By default the app runs with debug mode **off** and listens on `127.0.0.1` only. For local development you can opt in:

```bash
FLASK_DEBUG=1 python app.py                 # enable debug mode
FLASK_HOST=0.0.0.0 python app.py            # listen on all interfaces (only on a trusted network)
```

## Current Limitations

- Tasks are stored in a Python list in memory, so all data is lost on restart.
- No user accounts or authentication; all visitors share the same list.
- No automated tests.
- The page loads Tailwind CSS and Font Awesome from public CDNs, so it needs an internet connection.

## Future Improvements

- Persist tasks in SQLite
- User accounts
- Deployment guide

## Credits

The interface text credits Grok for the design (`صمم بواسطة Grok`), and that attribution is kept as it was in the original project.

## Author

Aymen — [github.com/aymnb7178](https://github.com/aymnb7178)
