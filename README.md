# FestFlow Web Application
Local Flask website connected to your existing MySQL database `fest_db`.

## Run on Windows
1. Start MySQL and confirm `fest_db` contains the tables and sample records.
2. Open `app.py` and replace `YOUR_MYSQL_PASSWORD` with your MySQL password (or set environment variable `DB_PASSWORD`). Never upload your password to GitHub.
3. Open Command Prompt in this folder and run:
   ```
   python -m venv .venv
   .venv\\Scripts\\activate
   pip install -r requirements.txt
   python app.py
   ```
4. Open http://127.0.0.1:5000

Pages: dashboard, events, students, registrations and payments.
Registration inserts use the MySQL triggers already created in `fest_db`.
This starter has not been tested against your local server from this environment. If a page reports a missing column/table, share the exact error so we can align it with your schema.
