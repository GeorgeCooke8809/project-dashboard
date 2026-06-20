import os
from dotenv import load_dotenv

load_dotenv("config.env")

DATABASE_URL = os.getenv("DATABASE_URL")
DEBUGGING_STATE = bool(os.getenv("DEBUGGING"))

if __name__ == "__main__":
    print("hello")