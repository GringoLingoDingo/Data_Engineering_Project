# App/main.py
import os
import numpy as np
from flask import Flask, request, jsonify, g
from .model_loader import load_model, load_all_metadata
from .preprocessing import preprocess_input
from .database import init_db, get_db, close_connection, log_prediction

app = Flask(__name__)

# --- Configuration ---
MODEL_COPIES_SOLD_NAME = 'catboost_model_Copies Sold.pkl'
MODEL_PREDICTS_LOG_TRANSFORMED = True # Keep as is, adjust if needed

# --- Global Variables for Models and Metadata ---
LOADED_COPIES_SOLD_MODEL = None
LOADED_METADATA = None

# --- Application Context Teardown ---
app.teardown_appcontext(close_connection)

# --- App Startup: Load Models and Initialize DB (Revised for Flask 2.3+) ---
# This code will execute once when the module is imported/run.
print("Initializing application (Flask 2.3+ method)...")

# Initialize database
# Call init_db directly here, as it doesn't strictly need app_context for connection setup
# (it creates a new connection, runs, then closes, which is fine for schema creation)
init_db()

# Load metadata first, as models often depend on it
try:
    LOADED_METADATA = load_all_metadata()
    print(f"Loaded {len(LOADED_METADATA.get('feature_columns', []))} feature columns.")
except Exception as e:
    print(f"FATAL ERROR: Could not load metadata. Exiting. {e}")
    exit(1)

# Load Copies Sold model
try:
    LOADED_COPIES_SOLD_MODEL = load_model(MODEL_COPIES_SOLD_NAME)
except Exception as e:
    print(f"FATAL ERROR: Could not load model '{MODEL_COPIES_SOLD_NAME}'. Exiting. {e}")
    exit(1)

print("Application initialized successfully.")


# --- API Endpoints ---
# ... (rest of your API endpoints remain the same) ...

@app.route('/')
def index():
    """Landing page providing API usage information."""
    example_features = {
        "time_to_beat": 120.0,
        "price": 29.99,
        "followers": 150000,
        "engagement_ratio": 2.1,
        "selected_tags": ["Survival", "Action"],
        "selected_genres": ["Adventure"],
        "selected_categories": ["Single-player"],
        "selected_publisher": "PublisherA"
    }
    # Attempt to get some actual values for display if metadata loaded
    if LOADED_METADATA:
        if LOADED_METADATA.get('tags'):
            example_features["selected_tags"] = [LOADED_METADATA['tags'][0]] if LOADED_METADATA['tags'] else []
        if LOADED_METADATA.get('genres'):
            example_features["selected_genres"] = [LOADED_METADATA['genres'][0]] if LOADED_METADATA['genres'] else []
        if LOADED_METADATA.get('categories'):
            example_features["selected_categories"] = [LOADED_METADATA['categories'][0]] if LOADED_METADATA['categories'] else []
        if LOADED_METADATA.get('publishers'):
            example_features["selected_publisher"] = LOADED_METADATA['publishers'][0] if LOADED_METADATA['publishers'] else "PublisherA"


    return jsonify({
        "message": "Welcome to the Game Metrics Prediction API!",
        "endpoints": {
            "/": "This landing page.",
            "/predict_copies_sold": {
                "method": "POST",
                "description": "Predict the number of copies sold based on game features.",
                "request_body": "JSON object with keys for numerical features and lists for selected categorical features. "
                                "Refer to 'feature_columns.csv', 'tags_list.csv', 'genres_list.csv', 'categories_list.csv', 'publisher_list.csv' for valid values.",
                "example_request": example_features,
                "response": "JSON object with 'prediction_copies_sold' and 'input_data'."
            }
        },
        "model_info": f"Main Model: {MODEL_COPIES_SOLD_NAME} (predicts log-transformed copies if configured)",
        "loaded_feature_columns_count": len(LOADED_METADATA.get('feature_columns', [])) if LOADED_METADATA else "Not loaded",
        "notes": "Ensure your 'selected_tags', 'selected_genres', 'selected_categories', 'selected_publisher' values match the exact strings in your metadata CSVs."
    })

@app.route('/predict_copies_sold', methods=['POST'])
def predict_copies_sold():
    """Endpoint for making predictions using the loaded copies sold model."""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    raw_input_data = request.get_json()

    # Model and metadata should already be loaded at app startup.
    # We still check here for robustness in case of an extremely rare race condition
    # or if startup failed silently (though we added exits for fatal errors).
    if LOADED_COPIES_SOLD_MODEL is None or LOADED_METADATA is None:
        return jsonify({"error": "Server not fully initialized. Model or metadata missing."}), 503

    try:
        processed_input_df = preprocess_input(raw_input_data, LOADED_METADATA)
        prediction_value = LOADED_COPIES_SOLD_MODEL.predict(processed_input_df)[0]

        if MODEL_PREDICTS_LOG_TRANSFORMED:
            prediction_value = np.expm1(prediction_value)
            prediction_value = max(0, prediction_value)

        db = get_db()
        log_prediction(raw_input_data, float(prediction_value))

        return jsonify({
            "prediction_copies_sold": round(float(prediction_value), 2),
            "input_data": raw_input_data
        })
    except ValueError as ve:
        return jsonify({"error": f"Input validation/preprocessing error: {str(ve)}. Please check your input against the expected format."}), 400
    except KeyError as ke:
        return jsonify({"error": f"Missing or invalid key in input data: {ke}. Ensure all required numerical features and optional lists/strings for categories are present and correctly named."}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected server error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    # When running directly with `python App/main.py`, the code above this block executes.
    # For `flask run`, this block is generally not used, as Flask handles the server.
    # However, if you wanted to keep this, ensure init logic is not duplicated.
    # The current setup where init_db etc. are called at module level is best.
    app.run(host='0.0.0.0', port=5000, debug=True)
