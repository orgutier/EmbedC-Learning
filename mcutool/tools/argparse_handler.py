import argparse
import sys
import os
from tools import logger

class CustomArgumentParser(argparse.ArgumentParser):
    def __init__(self):
        self.log = logger.logger()
        notifyname = None
        notifyid = None
        try:
            self.log.appname = os.path.basename(__file__)
        except Exception as e:
            # No problem, use default
            log.appname = "mcutool"
            notifyname = e
        try:
            log.taskid = int(os.getpid())
        except Exception as e:
            # No problem, use default
            log.taskid = 0000
            notifyid = e

        if notifyname:
            log.log( level = log.WARN, message = "appname was not defined, using default")
            log.log( level = log.WARN, message = f"Error: {notifyname}")
        if notifyid:
            log.log(level = log.WARN, message = "taskid was not defined, using default")
            log.log( level = log.WARN, message = f"Error: {notifyid}")

    def error(self, message):
        log.log(level=log.CRITICAL, message=f"Argument parsing error: {message}")
        self.print_help()
        sys.exit(2)