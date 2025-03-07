from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Database connection details
DB_HOST = os.getenv("DB_HOST", "postgres")
DB_NAME = os.getenv("DB_NAME", "mydatabase")
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# Ensure table exists
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS metrics (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP NOT NULL,
            containername TEXT NOT NULL,
            cpupercent FLOAT NOT NULL,
            rambytes BIGINT NOT NULL
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

@app.route("/", methods=["POST"])
def submit_data():
    data = request.get_json()
    if not data or not all(key in data for key in ["timestamp", "containername", "cpupercent", "rambytes"]):
        return jsonify({"error": "Invalid JSON format"}), 400
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO metrics (timestamp, containername, cpupercent, rambytes) VALUES (%s, %s, %s, %s)",
                    (data["timestamp"], data["containername"], data["cpupercent"], data["rambytes"]))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Data inserted successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8080, debug=True)
