from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_logs():
    conn = sqlite3.connect("safety.db")
    cursor = conn.cursor()
    rows = cursor.execute("SELECT * FROM safety_logs").fetchall()
    conn.close()
    return rows

@app.route('/')
def index():
    data = get_logs()
    return render_template("index.html", logs=data)

if __name__ == '__main__':
    app.run(debug=True)
