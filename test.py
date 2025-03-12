from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import sqlite3
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from career_assistant import handle_query  

app = Flask(__name__)
app.secret_key = r"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"
CORS(app)  


try:
    df = pd.read_csv(r"C:\Users\konda\OneDrive\Desktop\hackathon\career_guidance_dataset.csv")
    print("CSV Loaded Successfully!")
    print(df.head())  
except Exception as e:
    print(f"Error loading dataset: {e}")
    df = pd.DataFrame(columns=["Student Level", "Interest Area", "Suggested Subjects", "Recommended Courses",
                               "Career Options", "Govt Job Options", "Business Ideas", "Political Career Paths"])



def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()


@app.route("/")
def home1():
    return render_template("home1.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        if not username or not email or not password:
            return "All fields are required!", 400

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
                           (username, email, hashed_password))
            conn.commit()
            conn.close()
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            return "Username or email already exists!", 400

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            return "Both email and password are required!", 400

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session["user_id"] = user[0]
            session["username"] = user[1]
            return redirect(url_for("home1"))
        else:
            return "Invalid email or password!", 401

    return render_template("login.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('logout_page'))

@app.route('/logout_page')
def logout_page():
    return render_template('logout.html')

@app.route("/index")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", username=session.get("username"))

@app.route("/courses")
def courses():
    return render_template("courses.html")

@app.route("/career_paths")
def career_paths():
    return render_template("career_paths.html")

@app.route("/explore")
def explore():
    return render_template("explore.html")

@app.route("/expert_tips")
def expert_tips():
    return render_template("expert_tips.html")

@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

try:
    df = pd.read_csv(r"C:\Users\konda\OneDrive\Desktop\hackathon\career_guidance_dataset (1).csv")
except Exception as e:
    print(f"Error loading dataset: {e}")
    df = pd.DataFrame(columns=["Student Level", "Interest Area", "Suggested Subjects", "Recommended Courses", "Career Options", "Govt Job Options", "Business Ideas", "Political Career Paths"])


def get_career_guidance(education_level, interest_area):
    """Fetch career guidance based on education level and interest area."""
    education_level = education_level.strip().lower()
    interest_area = interest_area.strip().lower()

    df["Student Level"] = df["Student Level"].astype(str).str.strip().str.lower()
    df["Interest Area"] = df["Interest Area"].astype(str).str.strip().str.lower()

    filtered_data = df[(df["Student Level"] == education_level) & (df["Interest Area"] == interest_area)]

    if filtered_data.empty:
        return {"message": "No matching career guidance found. Try different inputs!"}

    career_info = filtered_data.drop(columns=["Student Level", "Interest Area"])
    return career_info.to_dict(orient="records")


@app.route("/get-career-guidance", methods=["POST"])
def career_guidance():
    """API endpoint to get career guidance based on user input."""
    data = request.json
    education_level = data.get("education_level")
    interest_area = data.get("interest_area")

    if not education_level or not interest_area:
        return jsonify({"error": "Missing required fields"}), 400

    response = get_career_guidance(education_level, interest_area)
    return jsonify(response)



@app.route('/chatbot-response', methods=['POST'])
def chatbot_response():
    data = request.get_json()
    user_query = data.get("query", "")

    if not user_query:
        return jsonify({"response": "Please ask a career-related question!"})

    response = handle_query(user_query)  
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
