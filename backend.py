import re
import random
import secrets
import hashlib
import sqlite3
import math
import string 
import base64
import urllib.parse
from zxcvbn import zxcvbn 
from flask import Flask, render_template, request, url_for

app = Flask(__name__)

# --- Database Logic ---
def get_db():
    conn = sqlite3.connect("nexus.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS logs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    detail TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
     """)
    conn.commit()
    conn.close() 

def log_event(log_type, detail):
    """Inserts a new log entry into the database."""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO logs (type, detail) VALUES (?, ?)", (log_type, detail))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Logging Error: {e}")

def export_logs():
        
        conn=get_db()
        cursor=conn.cursor()
        cursor.execute("SELECT id,type,detail,created_at from logs ORDER BY id")
        rows=cursor.fetchall()
        conn.close()
        
        with open("log.txt","w") as f:
            for row in rows:
                f.write(f"{row['id']} - {row['type']} - {row['detail']} - {row['created_at']}\n")
    
# --- Logic Functions ---

def logic_generate_password(length):
    try:
        # Enforce limits
        if length < 8: return "Error: Length must be > 5"
        if length > 100: length = 100 # CAP AT 100
        
        symbols = "!@#$%&*()"
        character_set = string.ascii_uppercase + string.ascii_lowercase + string.digits + symbols
        
        password = []
        password.append(secrets.choice(string.ascii_lowercase))
        password.append(secrets.choice(string.ascii_uppercase))
        password.append(secrets.choice(string.digits))
        password.append(secrets.choice(symbols))
        
        left_pass = length - 4
        password.extend([secrets.choice(character_set) for _ in range(left_pass)])
        
        random.shuffle(password)
        return "".join(password)
    except:
        return "Generation Error"

def logic_analyze_policy(password):
    if len(password) < 8: return {"is_valid": False, "Message": "Min 8 characters"}
    if not re.search(r'[A-Z]', password): return {"is_valid": False, "Message": "Need Uppercase"}
    if not re.search(r'[a-z]', password): return {"is_valid": False, "Message": "Need lowercase"}
    if not re.search(r'\d', password): return {"is_valid": False, "Message": "Need Digit"} 
    return {"is_valid": True, "Message": "Policy met"}

def password_analyze(password):
    strength = zxcvbn(password)
    score_rating = {0: "Terrible", 1: "Weak", 2: "Average", 3: "Good", 4: "Strong"}
    return {
        "score": strength['score'], 
        "rating": score_rating.get(strength['score'], "Weak"), 
        "Crack Time": strength['crack_times_display']['online_throttling_100_per_hour'], 
        "suggestions": strength['feedback']['suggestions']
    }

def hash_converter(text, algo):
    try:
        if algo not in hashlib.algorithms_available: return "Algo not supported"
        h = hashlib.new(algo)
        h.update(text.encode('utf-8'))
        return h.hexdigest()
    except Exception as e: return str(e)

def logic_base(text, choice, mode):
    try:
        b = text.encode('utf-8')
        if mode == 'encode':
            if choice == '1': return base64.b64encode(b).decode('utf-8')
            if choice == '2': return base64.b32encode(b).decode('utf-8')
            if choice == '3': return base64.b16encode(b).decode('utf-8')
            if choice == '4': return urllib.parse.quote(text)
        else: # decode
            if choice == '1': return base64.b64decode(text).decode('utf-8')
            if choice == '2': return base64.b32decode(text).decode('utf-8')
            if choice == '3': return base64.b16decode(text).decode('utf-8')
            if choice == '4': return urllib.parse.unquote(text)
    except: return "Decoding Error"
    return "Invalid"

def logic_brute_force(length, charset_size, rate):
    try:
        combinations = math.pow(charset_size, length)
        seconds = combinations / rate
        if seconds < 60: return f"{seconds:.2f} Seconds"
        if seconds < 3600: return f"{seconds/60:.2f} Minutes"
        if seconds < 86400: return f"{seconds/3600:.2f} Hours"
        if seconds < 31536000: return f"{seconds/86400:.2f} Days"
        return f"{int(seconds/31536000)} Years"
    except: return "Infinity"

# --- Routes ---

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["GET", "POST"])
def generate_password():
    result = ""
    if request.method == "POST":
        length = int(request.form.get("length", 0))
        if length > 5:
            result = logic_generate_password(length)
            # LOG THE EVENT
            log_event("Generator ", f"Generated pass length: {length} ")
    return render_template("generator.html", result=result)

@app.route("/analyzer", methods=["GET", "POST"])
def analyzer():
    result = None
    if request.method == "POST":
        pw = request.form.get("password")
        if pw:
            policy = logic_analyze_policy(pw)
            if policy["is_valid"]:
                data = password_analyze(pw)
                result = {"is_valid": True, "rating": data["rating"], "Score": data["score"], 
                          "Crack_time": data["Crack Time"], "suggestions": data["suggestions"]}
                # LOG THE EVENT
                log_event("Analyzer", f"Analyzed pass score: {data['score']}")
            else:
                result = {"is_valid": False, "Msg": policy["Message"]}
                log_event("Analyzer", "Failed policy check")
    return render_template("analyzer.html", result=result)

@app.route("/hashc", methods=["POST", "GET"])
def page_hash():
    output = ""
    if request.method == "POST":
        txt = request.form.get("text")
        algo = request.form.get("algorithm")
        if txt and algo:
            output = hash_converter(txt, algo)
            # LOG THE EVENT
            log_event("Hash", f"Converted to {algo}")
    return render_template("hashconverter.html", result=output)

@app.route("/base", methods=["POST", "GET"])
def page_base():
    output = ""
    if request.method == "POST":
        txt = request.form.get("text")
        mode = request.form.get("mode")
        choice = request.form.get("choice")
        if txt and mode and choice:
            output = logic_base(txt, choice, mode)
            # LOG THE EVENT
            log_event("BaseEncoding", f"{mode} operation")
    return render_template("base.html", result=output)

@app.route("/brute_force", methods=["POST", "GET"])
def page_brute():
    output = ""
    if request.method == "POST":
        try:
            l = int(request.form.get("length"))
            r = float(request.form.get("Rate"))
            c = int(request.form.get("charset"))
            c_map = {1:26, 2:52, 3:62, 4:95}
            output = logic_brute_force(l, c_map.get(c, 95), r)
            # LOG THE EVENT
            log_event("BruteForce", f"Est time for len {l}")
        except: output = "Error"
    return render_template("bruteforcetime.html", result=output)

@app.route("/terms",methods=["POST","GET"])
def page_terms():
    return render_template("terms.html")

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

export_logs()
