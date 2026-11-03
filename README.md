# Todo App (Flask)

A small task-management web app built with Flask and Tailwind CSS, with an Arabic right-to-left interface. Tasks are stored in a local SQLite file, so they survive restarts.

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
├── app.py              # Flask app factory, SQLite storage and routes
├── tests/              # unit tests (Flask test client, temporary database)
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

## Tests

```bash
python -m unittest -v     # 8 tests: add / toggle / delete, persistence across app instances,
                          # blank input, HTML escaping, length limit, SQL-injection attempt
```

> The SQLite storage and the tests were added with AI assistance (Claude), reviewed and published by the repository owner.

## Current Limitations

- Storage is a single local SQLite file (`todos.db`, override with `TODO_DB`); fine for one user, not a multi-server setup.
- No user accounts or authentication; all visitors share the same list.
- The page loads Tailwind CSS and Font Awesome from public CDNs, so it needs an internet connection.

## Future Improvements

- User accounts
- Deployment guide

## Credits

The interface text credits Grok for the design (`صمم بواسطة Grok`), and that attribution is kept as it was in the original project.

## Author

Aymen — [github.com/aymnb7178](https://github.com/aymnb7178)
