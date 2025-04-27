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
        # self.print_help()
        sys.exit(2)