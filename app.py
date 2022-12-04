from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Connect to the SQLite database
conn = sqlite3.connect("feedings.db")

# Create the feedings table if it doesn't exist
conn.execute("""
  CREATE TABLE IF NOT EXISTS feedings (
    time TEXT PRIMARY KEY,
    amount REAL
  )
""")

@app.route("/feedings", methods=["POST"])
def add_feeding():
  # Get the feeding data from the request body
  data = request.get_json()
  if not data:
    return jsonify({"error": "Invalid request body"}), 400

  # Add the feeding to the database
  conn.execute("""
    INSERT INTO feedings (time, amount) VALUES (?, ?)
  """, (data["time"], data["amount"]))
  conn.commit()

  return jsonify({"success": True}), 201

@app.route("/feedings/<time>", methods=["GET"])
def get_feeding(time):
  # Get the feeding with the specified time from the database
  cursor = conn.execute("""
    SELECT time, amount FROM feedings WHERE time = ?
  """, (time,))
  result = cursor.fetchone()
  if not result:
    return jsonify({"error": "Feeding not found"}), 404

  # Return the feeding data
  time, amount = result
  return jsonify({"time": time, "amount": amount}), 200

if __name__ == "__main__":
  app.run()
