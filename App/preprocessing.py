# App/preprocessing.py
import numpy as np
import pandas as pd

def preprocess_input(raw_input: dict, metadata: dict):
    """
    Preprocesses raw input data from an API request into a format
    suitable for the CatBoost model. This mimics the Streamlit app's logic.

    Args:
        raw_input (dict): A dictionary from the incoming JSON request,
                          e.g., {"time_to_beat": 60.0, "price": 19.99,
                                 "followers": 100000, "engagement_ratio": 1.5,
                                 "selected_tags": ["Survival", "Action"],
                                 "selected_genres": ["Adventure", "Indie"],
                                 "selected_categories": ["Single-player"],
                                 "selected_publisher": "PublisherA"}
        metadata (dict): A dictionary containing 'feature_columns', 'tags', 'genres',
                         'categories', 'publishers' lists loaded from metadata files.

    Returns:
        pd.DataFrame: A pandas DataFrame ready for model prediction,
                      with all expected feature columns in order.

    Raises:
        ValueError: If essential features are missing or data types are incorrect.
    """
    feature_columns = metadata.get('feature_columns')
    all_tags = metadata.get('tags')
    all_genres = metadata.get('genres')
    all_categories = metadata.get('categories')
    all_publishers = metadata.get('publishers')

    if not feature_columns:
        raise ValueError("Feature columns metadata is missing. Cannot preprocess input.")

    # Initialize a DataFrame with zeros for all expected feature columns
    # This handles one-hot encoding by default (all zeros, then set 1 for selected)
    input_df = pd.DataFrame(np.zeros((1, len(feature_columns))), columns=feature_columns)

    # Extract numerical features and set them directly
    numerical_features = {
        "time_to_beat": float(raw_input.get("time_to_beat", 0.0)),
        "Price": float(raw_input.get("price", 0.0)),
        "Followers": float(raw_input.get("followers", 0.0)),
        "engagement_ratio": float(raw_input.get("engagement_ratio", 0.0))
    }
    for col, value in numerical_features.items():
        if col in input_df.columns:
            input_df.at[0, col] = value
        else:
            print(f"Warning: Numerical column '{col}' not found in feature_columns. Skipping.")

    # Handle one-hot encoded categorical features
    # Publishers Class
    selected_publisher = raw_input.get("selected_publisher")
    if selected_publisher and selected_publisher in all_publishers:
        col = f"Publishers Class_{selected_publisher}"
        if col in input_df.columns:
            input_df.at[0, col] = 1
        else:
            print(f"Warning: Publisher column '{col}' not found in feature_columns.")

    # Tags
    selected_tags = raw_input.get("selected_tags", [])
    for tag in selected_tags:
        if tag in all_tags: # Validate tag against known tags
            col = f"Tags_{tag}"
            if col in input_df.columns:
                input_df.at[0, col] = 1
            else:
                print(f"Warning: Tag column '{col}' not found in feature_columns.")
        else:
            print(f"Warning: Provided tag '{tag}' is not in known tags_list.csv.")

    # Genres
    selected_genres = raw_input.get("selected_genres", [])
    for genre in selected_genres:
        if genre in all_genres: # Validate genre against known genres
            col = f"genres_{genre}"
            if col in input_df.columns:
                input_df.at[0, col] = 1
            else:
                print(f"Warning: Genre column '{col}' not found in feature_columns.")
        else:
            print(f"Warning: Provided genre '{genre}' is not in known genres_list.csv.")

    # Categories
    selected_categories = raw_input.get("selected_categories", [])
    for category in selected_categories:
        if category in all_categories: # Validate category against known categories
            col = f"categories_{category}"
            if col in input_df.columns:
                input_df.at[0, col] = 1
            else:
                print(f"Warning: Category column '{col}' not found in feature_columns.")
        else:
            print(f"Warning: Provided category '{category}' is not in known categories_list.csv.")

    # Final check: Ensure the DataFrame has the exact columns in the correct order
    # and convert to float as per your Streamlit app.
    try:
        input_df = input_df[feature_columns]
        input_df = input_df.astype(float)
    except KeyError as e:
        raise ValueError(f"Feature mismatch: Expected column '{e}' not found after preprocessing. "
                         "This might indicate an issue with feature_columns.csv or input data.")
    except Exception as e:
        raise ValueError(f"Error during final input DataFrame processing: {e}")

    # CatBoost models can often take pandas DataFrames directly.
    # If not, convert to numpy array: input_df.values
    return input_df

if __name__ == '__main__':
    # --- Example Usage for Testing ---
    # Dummy metadata for testing purposes (in a real scenario, these would be loaded from files)
    dummy_metadata = {
        'feature_columns': [
            'time_to_beat', 'Price', 'Followers', 'engagement_ratio',
            'Publishers Class_PublisherA', 'Publishers Class_PublisherB',
            'Tags_Survival', 'Tags_Action', 'Tags_RPG',
            'genres_Adventure', 'genres_Indie', 'genres_Strategy',
            'categories_Single-player', 'categories_Multi-player'
        ],
        'tags': ['Survival', 'Action', 'RPG'],
        'genres': ['Adventure', 'Indie', 'Strategy'],
        'categories': ['Single-player', 'Multi-player'],
        'publishers': ['PublisherA', 'PublisherB']
    }

    # Example 1: Full valid input
    print("--- Test 1: Full Valid Input ---")
    raw_input_1 = {
        "time_to_beat": 120.0,
        "price": 29.99,
        "followers": 150000,
        "engagement_ratio": 2.1,
        "selected_tags": ["Survival", "RPG"],
        "selected_genres": ["Adventure"],
        "selected_categories": ["Single-player", "Multi-player"],
        "selected_publisher": "PublisherA"
    }
    try:
        processed_data_1 = preprocess_input(raw_input_1, dummy_metadata)
        print("Processed Data 1 (head and dtypes):\n", processed_data_1.head())
        print(processed_data_1.dtypes)
        print("Shape:", processed_data_1.shape)
        # Expected: A DataFrame with 1 row, 14 columns, with correct 1s set.
    except ValueError as e:
        print(f"Error in Test 1: {e}")

    # Example 2: Missing optional categorical selections
    print("\n--- Test 2: Missing Optional Selections ---")
    raw_input_2 = {
        "time_to_beat": 50.0,
        "price": 9.99,
        "followers": 50000,
        "engagement_ratio": 0.8,
        # No tags, genres, categories, publisher
    }
    try:
        processed_data_2 = preprocess_input(raw_input_2, dummy_metadata)
        print("Processed Data 2 (head and dtypes):\n", processed_data_2.head())
        print(processed_data_2.dtypes)
        print("Shape:", processed_data_2.shape)
        # Expected: A DataFrame with 1 row, 14 columns, mostly zeros for categorical.
    except ValueError as e:
        print(f"Error in Test 2: {e}")

    # Example 3: Invalid tag/genre/category/publisher (should show warnings, but still process)
    print("\n--- Test 3: Invalid Categorical Input ---")
    raw_input_3 = {
        "time_to_beat": 300.0,
        "price": 59.99,
        "followers": 500000,
        "engagement_ratio": 3.5,
        "selected_tags": ["NonExistentTag"], # Will print warning
        "selected_genres": ["NonExistentGenre"],
        "selected_publisher": "NonExistentPublisher"
    }
    try:
        processed_data_3 = preprocess_input(raw_input_3, dummy_metadata)
        print("Processed Data 3 (head and dtypes):\n", processed_data_3.head())
        print(processed_data_3.dtypes)
        print("Shape:", processed_data_3.shape)
    except ValueError as e:
        print(f"Error in Test 3: {e}")

    # Example 4: Missing required numerical feature (should raise ValueError)
    print("\n--- Test 4: Missing Required Numerical Feature ---")
    raw_input_4 = {
        "price": 1.0,
        "followers": 100
        # time_to_beat and engagement_ratio are missing
    }
    try:
        processed_data_4 = preprocess_input(raw_input_4, dummy_metadata)
        print("Processed Data 4:\n", processed_data_4)
    except ValueError as e:
        print(f"Caught expected error in Test 4: {e}")