# Game Metrics Prediction API

This project deploys a Machine Learning model as a REST API using Flask. The API allows users to predict the number of copies a game might sell based on various features. The application is Dockerized, and all predictions are logged into a SQLite database.

## Table of Contents

-   [Objective](#objective)
-   [Architecture Overview](#architecture-overview)
-   [Features](#features)
-   [Project Structure](#project-structure)
-   [Getting Started](#getting-started)
    -   [Prerequisites](#prerequisites)
    -   [Local Setup (Without Docker)](#local-setup-without-docker)
    -   [Running with Docker](#running-with-docker)
-   [API Endpoints](#api-endpoints)
-   [Database](#database)
-   [DockerHub](#dockerhub)
-   [Deliverables](#deliverables)
-   [Contributing](#contributing)
-   [License](#license)

## Objective

The primary objective of this project is to demonstrate the deployment of a Machine Learning model as a RESTful API. Key requirements include:

* Serving a pre-trained ML model (CatBoost) via a REST API.
* Providing clear API endpoints for interaction.
* Including a persistent database (SQLite) for logging predictions.
* Containerizing the application using Docker.
* Making the Docker image available on DockerHub.
* Providing a user-friendly landing page for API access instructions.

## Architecture Overview

The system is designed with a clear separation of concerns, encapsulating the ML model, preprocessing logic, and database interactions within a Flask API, all deployed via Docker.

+---------------------+       HTTP POST (JSON)        +--------------------------------+
|       Client        |------------------------------>|         Docker Container       |
| (Browser/Postman)   |                               |      (Game Metrics API)        |
+---------------------+                               |                                |
|   +--------------------------+   |
|   |     Flask Application    |   |
|   |     (App/main.py)        |   |
|   +--------------------------+   |
|              |                   |
|              v                   |
|   +--------------------------+   |
|   |   Preprocessing Logic    |   |
|   |   (App/preprocessing.py) |   |
|   +--------------------------+   |
|     ^           |              |
|     |           v              |
|   +-------+   +--------------+   |
|   |Metadata|-->| ML Model     |   |
|   |(CSV lists)| (CatBoost)     |   |
|   +-------+   |(Copies Sold)   |   |
|               +--------------+   |
|                      |           |
|                      v           |
|   +--------------------------+   |
|   |     Database Logging     |   |
|   |     (App/database.py)    |   |
|   +--------------------------+   |
|              |                   |
|              v                   |
|   +--------------------------+   |
|   |   SQLite Database        |   |
|   |   (database.db)          |   |
|   +--------------------------+   |
|                                |
+---------------------+       HTTP JSON Response      |                                |
|       Client        |<------------------------------+--------------------------------+
| (Browser/Postman)   |       (Prediction)
+---------------------+


## Features

* **RESTful API:** Built with Flask, offering a `/predict_copies_sold` endpoint for model inference.
* **Game Metrics Prediction:** Utilizes a CatBoost model to predict the number of copies a game might sell.
* **Intelligent Preprocessing:** Handles complex input transformation (including one-hot encoding for categorical features) using metadata files (`metadata/`).
* **Prediction Logging:** All prediction requests and their corresponding outputs are logged to a local SQLite database (`database.db`).
* **Informative Landing Page:** The root endpoint (`/`) serves as a guide for API usage.
* **Dockerized Deployment:** The entire application is packaged into a Docker image for consistent and portable deployment.

## Project Structure

.
├── App/                            # Contains the core Flask application logic
│   ├── init.py                 # Makes 'App' a Python package
│   ├── database.py                 # Handles SQLite database connection and logging
│   ├── main.py                     # Main Flask application with API endpoints
│   ├── model_loader.py             # Functions to load ML models and metadata files
│   └── preprocessing.py            # Logic for transforming raw API input into model-ready features
├── Dockerfile                      # Defines how to build the Docker image
├── metadata/                       # Stores necessary data for preprocessing
│   ├── categories_list.csv
│   ├── feature_columns.csv         # Crucial: Lists all features in correct order for the model
│   ├── genres_list.csv
│   ├── publisher_list.csv
│   └── tags_list.csv
├── Trained_models/                 # Stores pre-trained machine learning models
│   └── catboost_model_Copies Sold.pkl # The primary model used for prediction
├── database.db                     # SQLite database file (generated on first run)
├── README.md                       # This project documentation file
└── requirements.txt                # Python dependencies for the project


## Getting Started

### Prerequisites

Ensure you have the following installed on your system:

* **Python 3.9+** (or compatible version used in `Dockerfile`)
* **pip** (Python package installer)
* **Docker Desktop** (for running with Docker)
* **Git** (for cloning the repository)

### Local Setup (Without Docker)

Follow these steps to run the application directly on your machine:

1.  **Clone the repository:**
    ```bash
    git clone [YOUR_GITHUB_REPO_URL]
    cd [YOUR_REPO_NAME] # e.g., cd Data_Engineering_Project
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate # On Windows PowerShell
    # source venv/bin/activate # On macOS/Linux/Git Bash
    ```

3.  **Install dependencies:**
    ```powershell
    pip install -r requirements.txt
    ```

4.  **Verify Model and Metadata Loading:**
    This step confirms your model and metadata files are correctly placed and readable.
    ```powershell
    python App/model_loader.py
    ```
    *Expected output should show successful loading of model and all metadata lists.*

5.  **Run the Flask application:**
    Set the `FLASK_APP` environment variable and run the Flask development server.
    ```powershell
    $env:FLASK_APP="App.main"
    python -m flask run --host=0.0.0.0 --port=5000
    ```
    The API will be available at `http://127.0.0.1:5000/`.

### Running with Docker

This is the recommended way to run the application, ensuring a consistent environment.

1.  **Ensure Docker Desktop is running** on your system.

2.  **Navigate to the project root** in your terminal.

3.  **Build the Docker image:**
    This command builds the Docker image based on your `Dockerfile`.
    ```powershell
    docker build -t [YOUR_DOCKERHUB_USERNAME]/game-metrics-api .
    ```
    *(Replace `[YOUR_DOCKERHUB_USERNAME]` with your actual DockerHub username.)*

4.  **Run the Docker container:**
    This command starts a container from your built image, mapping port 5000 from the container to your host.
    ```powershell
    docker run -p 5000:5000 [YOUR_DOCKERHUB_USERNAME]/game-metrics-api
    ```
    The API will be available at `http://localhost:5000/`.

## API Endpoints

### 1. Landing Page

* **URL:** `/`
* **Method:** `GET`
* **Description:** Provides an overview of the API and instructions on how to use the prediction endpoint.
* **Example Response (truncated):**
    ```json
    {
      "message": "Welcome to the Game Metrics Prediction API!",
      "endpoints": {
        "/": "...",
        "/predict_copies_sold": {
          "method": "POST",
          "description": "...",
          "example_request": {
            "engagement_ratio": 2.1,
            "followers": 150000,
            "price": 29.99,
            "selected_categories": ["Captions available"],
            "selected_genres": ["Action"],
            "selected_publisher": "AA",
            "selected_tags": ["1980s"],
            "time_to_beat": 120.0
          },
          "response": "..."
        }
      },
      "loaded_feature_columns_count": 508,
      "model_info": "Main Model: catboost_model_Copies Sold.pkl (predicts log-transformed copies if configured)",
      "notes": "..."
    }
    ```

### 2. Predict Copies Sold Endpoint

* **URL:** `/predict_copies_sold`
* **Method:** `POST`
* **Description:** Accepts game features and returns a predicted number of copies sold.
* **Request Body (JSON Example):**
    ```json
    {
      "time_to_beat": 120.0,
      "price": 29.99,
      "followers": 150000,
      "engagement_ratio": 2.1,
      "selected_tags": ["1980s"],
      "selected_genres": ["Action"],
      "selected_categories": ["Captions available"],
      "selected_publisher": "AA"
    }
    ```
    *Ensure values for `selected_tags`, `selected_genres`, `selected_categories`, and `selected_publisher` exist in their respective `metadata/*.csv` files.*

* **Example Request (using PowerShell):**
    ```powershell
    Invoke-WebRequest -Uri http://localhost:5000/predict_copies_sold -Method POST -ContentType "application/json" -Body '{
        "time_to_beat": 120.0,
        "price": 29.99,
        "followers": 150000,
        "engagement_ratio": 2.1,
        "selected_tags": ["1980s"],
        "selected_genres": ["Action"],
        "selected_categories": ["Captions available"],
        "selected_publisher": "AA"
    }'
    ```

* **Example Success Response (truncated):**
    ```json
    {
      "input_data": { /* ... input data ... */ },
      "prediction_copies_sold": 12345.67
    }
    ```

## Database

The application utilizes a `SQLite3` database (`database.db`) to log all prediction requests. The `predictions` table stores:

* `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
* `timestamp` (DATETIME DEFAULT CURRENT_TIMESTAMP)
* `input_data` (TEXT: JSON string of the input features)
* `prediction` (REAL: The predicted copies sold value)

## DockerHub

The Docker image for this application is available on DockerHub.

* **Repository Link:** `https://hub.docker.com/r/[YOUR_DOCKERHUB_USERNAME]/game-metrics-api`
* **To pull and run this image directly:**
    ```powershell
    docker pull [YOUR_DOCKERHUB_USERNAME]/game-metrics-api:latest
    docker run -p 5000:5000 [YOUR_DOCKERHUB_USERNAME]/game-metrics-api:latest
    ```
    *(Replace `[YOUR_DOCKERHUB_USERNAME]` with your actual DockerHub username.)*

## Deliverables

* GitHub repository with all source code and documentation.
* Functional REST API accessible locally.
* Deployed Machine Learning model (`catboost_model_Copies Sold.pkl`).
* Database integration (SQLite3 for prediction logging).
* Dockerized application with an image on DockerHub.
* Presentation slides and architecture diagram.

## Contributing

Feel free to fork this repository, open issues, and submit pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
