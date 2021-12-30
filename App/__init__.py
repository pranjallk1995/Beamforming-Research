import os
import logging

from App.main import main

if __name__ == "__main__":
    logging_path = os.path.join(os.getcwd(), "Logs", "App_logs.log")
    if os.path.isfile(logging_path):
        os.remove(logging_path)
    logging.basicConfig(filename = "Logs/App_logs.log", level = logging.INFO)
    main()