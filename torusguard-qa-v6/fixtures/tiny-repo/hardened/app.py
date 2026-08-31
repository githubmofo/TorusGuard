import os
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
SECRET_KEY = os.environ["APP_SECRET_KEY"]

def index():
    return "Welcome"
