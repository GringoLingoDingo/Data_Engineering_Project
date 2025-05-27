# App/model_loader.py
import joblib
import os
import pandas as pd # Needed for reading CSVs
# If your CatBoost models are stored as .cbm files and loaded using catboost.CatBoostRegressor.load_model,
# you'd import CatBoost here. But joblib.load typically works for .pkl files.
# from catboost import CatBoostRegressor # Uncomment if models are CatBoost objects saved directly

# Path to the base directory of models and metadata (relative to where main.py runs)
MODELS_DIR = 'Trained_models'
METADATA_DIR = 'metadata'

def load_model(model_name: str):
    """
    Loads a pre-trained model from the 'Trained_models' directory.
    Assumes the model is saved with joblib.
    """
    model_path = os.path.join(MODELS_DIR, model_name)
    try:
        # If your CatBoost models were saved as .cbm files, you'd use:
        # model = CatBoostRegressor().load_model(model_path)
        # But given your .pkl extension, joblib.load is correct.
        model = joblib.load(model_path)
        print(f"Model '{model_name}' loaded successfully from {model_path}.")
        return model
    except FileNotFoundError:
        print(f"Error: Model file not found at {model_path}. Please check path and file name.")
        raise
    except Exception as e:
        print(f"Error loading model '{model_name}': {e}")
        raise

def load_list_from_csv(file_name: str):
    """
    Loads a list of strings from a CSV file in the 'metadata' directory.
    Assumes it's a single column CSV.
    """
    file_path = os.path.join(METADATA_DIR, file_name)
    try:
        # Using .squeeze().tolist() as shown in your Streamlit app
        data_list = pd.read_csv(file_path, header=None).squeeze().tolist()
        print(f"List from '{file_name}' loaded successfully.")
        return data_list
    except FileNotFoundError:
        print(f"Error: Metadata file not found at {file_path}. Please check path and file name.")
        raise
    except Exception as e:
        print(f"Error loading list from '{file_name}': {e}")
        raise

def load_all_metadata():
    """
    Loads all necessary metadata lists for preprocessing.
    """
    metadata = {}
    try:
        metadata['feature_columns'] = load_list_from_csv("feature_columns.csv")
        metadata['tags'] = load_list_from_csv("tags_list.csv")
        metadata['genres'] = load_list_from_csv("genres_list.csv")
        metadata['categories'] = load_list_from_csv("categories_list.csv")
        metadata['publishers'] = load_list_from_csv("publisher_list.csv")
        print("All metadata lists loaded successfully.")
        return metadata
    except Exception as e:
        print(f"Error loading all metadata: {e}")
        raise

if __name__ == '__main__':
    # Example usage:
    try:
        # Remember to account for the space in the model file name
        loaded_model = load_model("catboost_model_Copies Sold.pkl")
        print(f"Type of loaded model: {type(loaded_model)}")
    except Exception as e:
        print(f"Failed to load model during test: {e}")

    try:
        loaded_metadata = load_all_metadata()
        print(f"Loaded feature columns: {loaded_metadata.get('feature_columns')[:5]}...") # show first 5
        print(f"Loaded genres: {loaded_metadata.get('genres')[:5]}...")
    except Exception as e:
        print(f"Failed to load metadata during test: {e}")