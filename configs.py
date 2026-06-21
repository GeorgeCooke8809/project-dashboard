import os
from dotenv import load_dotenv, set_key
from pathlib import Path
import logging

if os.path.isfile("config.env") != True: # Create new config if none exists
    logging.warning("config.env did not exist, creating with default settings...")

    env_file_path = Path("config.env")

    env_file_path.touch(mode=0o600, exist_ok=False)

    set_key(dotenv_path=env_file_path, key_to_set="DATABASE_URL", value_to_set="sqlite:///instance\projects.db")
    set_key(dotenv_path=env_file_path, key_to_set="DEBUGGING_STATE", value_to_set=False)
    set_key(dotenv_path=env_file_path, key_to_set="ADMIN_PASSWORD", value_to_set="adminpassword123*")
    set_key(dotenv_path=env_file_path, key_to_set="NETWORK_PORT", value_to_set=5000)


load_dotenv("config.env")

DATABASE_URL = os.getenv("DATABASE_URL")
logging.info(f"{DATABASE_URL = }")
DEBUGGING_STATE = bool(os.getenv("DEBUGGING"))
logging.info(f"{DEBUGGING_STATE = }")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
logging.info("Imported admin password to memory.")
NETWORK_PORT = os.getenv("NETWORK_PORT")
logging.info(f"{NETWORK_PORT = }")