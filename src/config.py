import os


class Config:
    MODEL = "gpt-4.1-mini"
    HIVETRACE_URL = os.getenv("HIVETRACE_URL", "http://localhost:8000")
    HIVETRACE_ACCESS_TOKEN = os.getenv(
        "HIVETRACE_ACCESS_TOKEN",
        "c612cc7dcbbb11ac10ea50d2b0822d0106e754b2a7bdbab058fee4fedeeebdb3",
    )
    HIVETRACE_APP_ID = os.getenv(
        "HIVETRACE_APP_ID", "60936f30-fdf5-4a5b-aabd-e2c423e9de44"
    )
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SESSION_ID = os.getenv("SESSION_ID")
    USER_ID = os.getenv("USER_ID")
