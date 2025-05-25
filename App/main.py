from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {
        "message": "Welcome to the Game Success Analytics API!",
        "usage": "See /docs for interactive API documentation."
    }