import os
from dotenv import load_dotenv

load_dotenv("config.env")

DATABASE_URL = os.getenv("DATABASE_URL")
DEBUGGING_STATE = bool(os.getenv("DEBUGGING"))
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")