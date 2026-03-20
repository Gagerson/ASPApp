# Automation Support Portal

A web-based helpdesk application for managing automation support tickets raised against UiPath and Power Automate robots. Built with Python, Flask and SQLite.

---

## Requirements

- Python 3.10 or higher
- pip

---

## Installation

1. Clone the repository or download and unzip the project files (https://github.com/Gagerson/ASPApp)

2. Open a terminal in the project root folder

3. Create a virtual environment:
   ```
   py -m venv .venv
   ```

4. Activate the virtual environment:
   - **Windows:** `.venv\Scripts\activate`
   - **Mac/Linux:** `source .venv/bin/activate`

5. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

---

## Running the Application

```
python app.py
```

The application will be available at: **https://aspapp.onrender.com/**

The database is created and seeded automatically on first run — no manual setup required.

---

## Running the Tests

```
pytest -v
```

The test suite uses an in-memory SQLite database and does not affect the application database. All 18 tests should pass on a clean install.

---

## Test Accounts

All accounts use the password: `password123`

| Name              | Email              | Role    |
|-------------------|--------------------|---------|
| Gandalf Grey      | gandalf@portal.com | Admin   |
| Aragorn Elessar   | aragorn@portal.com | Admin   |
| Arwen Undomiel    | arwen@portal.com   | Admin   |
| Frodo Baggins     | frodo@portal.com   | Regular |
| Samwise Gamgee    | sam@portal.com     | Regular |
| Legolas Greenleaf | legolas@portal.com | Regular |

---

## User Roles

**Regular users** can:
- Register and log in
- View all tickets
- Raise new tickets
- Edit existing tickets
- Add updates to tickets

**Admin users** can do everything above, plus:
- Delete tickets
- Add new robots

---

## Project Structure

```
app.py          — Flask application and route handlers
models.py       — Database models
validation.py   — Input validation functions
helpers.py      — Authentication decorators and utility functions
constants.py    — Allowed values for categories, statuses and platforms
db.py           — SQLAlchemy database instance
seed.py         — Sample data (seeded automatically on first run)
test_app.py     — Automated test suite (pytest)
templates/      — HTML templates
requirements.txt — Python dependencies
```

---

## Development Notes

- The `SECRET_KEY` in `app.py` should be replaced with a strong random value in production
- The database file `data.db` is created automatically in the instance folder on first run
- To reset the database, delete `data.db` and restart the application — it will reseed automatically
