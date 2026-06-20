import logging
logging.basicConfig(level=logging.DEBUG, filename="log.log", filemode="w", format="%(asctime)s - %(levelname)s - %(message)s")

import projects

if __name__ == "__main__":
    print("hello world")
    logging.info("Program running")