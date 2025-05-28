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
