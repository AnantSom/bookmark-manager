from flask import Flask, render_template, request, redirect, session
import os
import time
from dotenv import load_dotenv
import psycopg2

# --- App Initialization ---
app = Flask(__name__)
load_dotenv()  # Load environment variables from .env
app.secret_key = 'a_very_secret_key_for_the_website_manager'  # 🔐 Change this in production

# --- Database Connection ---
max_retries = 10
conn, cur = None, None

for i in range(max_retries):
    try:
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT", "5432")  # ✅ Use port from .env
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cur = conn.cursor()
        print(f"✅ [Website Manager] Connected to PostgreSQL at {db_host}:{db_port}")
        break
    except Exception as e:
        print(f"⏳ [Website Manager] Waiting for DB... ({i+1}/{max_retries}) - {e}")
        time.sleep(3)

if not conn:
    raise Exception("❌ [Website Manager] Could not connect to database after multiple attempts")

# --- Routes ---
@app.route('/')
def home():
    return redirect('/dashboard' if 'user_id' in session else '/login')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # 🔐 Use hashing (e.g., bcrypt) in production!
        try:
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            return redirect('/login')
        except psycopg2.Error:
            conn.rollback()
            return render_template('signup.html', error="Signup failed. Username might already exist.")
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur.execute("SELECT id, username FROM users WHERE username=%s AND password=%s", (username, password))
        user = cur.fetchone()
        if user:
            session['user_id'], session['username'] = user[0], user[1]
            return redirect('/dashboard')
        return render_template('login.html', error="Invalid username or password.")
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    message = ""
    user_id = session['user_id']

    try:
        if request.method == 'POST':
            if 'website' in request.form and 'name' in request.form:
                cur.execute("INSERT INTO websites (user_id, url, name) VALUES (%s, %s, %s)",
                            (user_id, request.form['website'], request.form['name']))
                message = "Website added!"
            elif 'delete_id' in request.form:
                cur.execute("DELETE FROM websites WHERE id = %s AND user_id = %s",
                            (request.form['delete_id'], user_id))
                message = "Website deleted."
            conn.commit()

        cur.execute("SELECT id, name, url FROM websites WHERE user_id = %s ORDER BY id", (user_id,))
        websites = cur.fetchall()
    except psycopg2.Error as e:
        conn.rollback()
        websites = []
        message = f"A database error occurred: {e}"

    return render_template('dashboard.html', username=session['username'], websites=websites, message=message)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# --- Main Execution ---
if __name__ == '__main__':
    port = int(os.getenv("PUBLIC_PORT", 10001))
    flask_port = int(os.getenv("FLASK_RUN_PORT", 10000))
    print(f"🔗 Access the app at: http://localhost:{port}")
    app.run(host="0.0.0.0", port=flask_port, debug=True)
