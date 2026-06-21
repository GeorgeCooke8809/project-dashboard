import logging
from datetime import datetime
from frontend import create_app
import configs
from configs import DEBUGGING_STATE, NETWORK_PORT

now = datetime.now().strftime("%d.%m.%Y-%H.%M.%S")
logging.basicConfig(level=logging.DEBUG, filename=f".\\logs\\{now}.log", filemode="w", format="%(asctime)s - %(levelname)s - %(pathname)s : %(funcName)s : %(lineno)d - %(message)s")

import projects

if __name__ == "__main__":
    logging.info("Program running")

    app = create_app()
    app.run(debug=DEBUGGING_STATE, port=NETWORK_PORT)