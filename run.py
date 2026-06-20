import os
from dotenv import load_dotenv

import logging
logging.basicConfig(level=logging.DEBUG, filename="log.log", filemode="w", format="%(asctime)s - %(levelname)s - %(message)s")

load_dotenv("config.env")

DATABASE_URL = os.getenv("DATABASE_URL")
DEBUGGING_STATE = bool(os.getenv("DEBUGGING"))

import projects

if __name__ == "__main__":
    print("hello world")
    logging.info("Program running")