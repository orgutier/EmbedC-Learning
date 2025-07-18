import argparse
import sys
import os
from tools.logger import logger

class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.log = logger(
            appname = os.path.basename(__file__),
            taskid = int(os.getpid())
        )
        self.log.log(level=self.log.CRITICAL, message=f"Argument parsing error: {message}")
        raise TypeError (f"Parsing error: {message}")
        # self.print_help()