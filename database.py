import sqlite3

conn = sqlite3.connect("safety.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS safety_logs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    workers INTEGER,
    helmets INTEGER,
    fire_status TEXT,
    violation TEXT
)
""")

conn.commit()
conn.close()
print("Database Created Successfully")
