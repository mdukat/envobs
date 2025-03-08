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
def init_container_table():
    print("Creating container_metrics table if it doesn't exist...")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS container_metrics (
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

def init_host_table():
    print("Creating host_metrics table if it doesn't exist...")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS host_metrics (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP NOT NULL,
            cpupercent FLOAT NOT NULL,
            rambytes BIGINT NOT NULL,
            maxrambytes BIGINT NOT NULL,
            swapbytes BIGINT NOT NULL,
            maxswapbytes BIGINT NOT NULL
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

def init_db():
    init_container_table()
    init_host_table()

@app.route("/container", methods=["POST"])
def submit_container_data():
    data = request.get_json()
    if not data or not all(key in data for key in ["timestamp", "containername", "cpupercent", "rambytes"]):
        return jsonify({"error": "Invalid JSON format"}), 400
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO container_metrics (timestamp, containername, cpupercent, rambytes) VALUES (%s, %s, %s, %s)",
                    (data["timestamp"], data["containername"], data["cpupercent"], data["rambytes"]))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Data inserted successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/host", methods=["POST"])
def submit_host_data():
    data = request.get_json()
    if not data or not all(key in data for key in ["timestamp", "swapbytes", "maxswapbytes", "cpupercent", "rambytes", "maxrambytes"]):
        return jsonify({"error": "Invalid JSON format"}), 400
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO host_metrics (timestamp, cpupercent, rambytes, maxrambytes, swapbytes, maxswapbytes) VALUES (%s, %s, %s, %s, %s, %s)",
                    (data["timestamp"], data["cpupercent"], data["rambytes"], data["maxrambytes"], data["swapbytes"], data["maxswapbytes"]))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Data inserted successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8080, debug=True)
