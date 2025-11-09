from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask app
app = Flask(__name__)
CORS(app)

DB_NAME = "data.db"

# --- Initialize Database ---
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password_hash TEXT,
                role TEXT
            )
        ''')
        conn.commit()
    print("✅ Database initialized")

# --- Add a user safely ---
def add_user(username, password, role):
    pwd_hash = generate_password_hash(password)
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cur = conn.cursor()
            cur.execute("INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                        (username, pwd_hash, role))
            conn.commit()
    except Exception as e:
        print("⚠️ Could not add user:", e)

# --- Routes ---

@app.route('/')
def home():
    return "✅ API is running! Use /register, /login, or /secure_data"

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username, password = data.get("username"), data.get("password")
    if not username or not password:
        return jsonify({"error": "Missing fields"}), 400

    pwd_hash = generate_password_hash(password)
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                        (username, pwd_hash, "user"))
            conn.commit()
        return jsonify({"message": "User registered"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "User already exists"}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username, password = data.get("username"), data.get("password")
    if not username or not password:
        return jsonify({"error": "Missing fields"}), 400

    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT password_hash, role FROM users WHERE username = ?", (username,))
        row = cur.fetchone()

    if row and check_password_hash(row[0], password):
        return jsonify({"message": "Login successful", "role": row[1]}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/secure_data', methods=['GET'])
def secure_data():
    return jsonify({"data": "This is protected data accessible after login!"})

# --- Start Server ---
if __name__ == '__main__':
    print("Initializing database...")
    init_db()
    add_user("testuser", "testpass", "user")
    add_user("admin", "adminpass", "admin")
    print("✅ Default users added")
    print("🚀 API running on http://127.0.0.1:5000")
    app.run(port=5000, debug=True)
