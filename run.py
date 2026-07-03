import logging
import os
from datetime import datetime
from frontend import create_app
import configs
from configs import DEBUGGING_STATE, NETWORK_PORT

root_logger = logging.getLogger()
root_logger.handlers.clear()

now = datetime.now().strftime("%d.%m.%Y-%H.%M.%S")

log_dir = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(level=logging.DEBUG, filename=os.path.join(log_dir, f"{now}.log"), filemode="w", format="%(asctime)s - %(levelname)s - %(pathname)s : %(funcName)s : %(lineno)d - %(message)s")
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logging.getLogger().addHandler(stream_handler)

import projects

if __name__ == "__main__":
    logging.critical("Program running")

    app = create_app()
    app.run(debug=DEBUGGING_STATE, port=NETWORK_PORT, use_reloader=False)