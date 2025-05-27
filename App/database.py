# App/database.py
import sqlite3
import json
import os
from flask import g

DATABASE = 'database.db' # This path is relative to where app.py is run

def get_db():
    """Connects to the specified database."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row # This allows us to access columns by name
    return db

def close_connection(exception):
    """Closes the database connection when the application context ends."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """Initializes the database schema."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            input_data TEXT,
            prediction REAL
        )
    ''')
    conn.commit()
    conn.close()
    print("Database initialized or already exists.")

def log_prediction(input_data: dict, prediction_value: float):
    """Logs a prediction to the database."""
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO predictions (input_data, prediction) VALUES (?, ?)",
            (json.dumps(input_data), prediction_value)
        )
        db.commit()
        print(f"Prediction logged: Input={input_data}, Prediction={prediction_value}")
    except Exception as e:
        db.rollback()
        print(f"Error logging prediction: {e}")

if __name__ == '__main__':
    # This block is for testing database initialization directly
    # In the main app, init_db() will be called once on startup
    init_db()
    # Example usage:
    # with get_db() as db:
    #     log_prediction({"feature1": 10, "feature2": 20}, 150.5)