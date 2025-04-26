import argparse
import os
from tools import enterboot, enterapp
from tools.logger import logger

log = logger()
notifyname = None
notifyid = None
try:
    log.appname = os.path.basename(__file__)
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

parser = argparse.ArgumentParser(
    description="MCU control tool")
group = parser.add_mutually_exclusive_group(required=True)

group.add_argument(
    '--enterboot', 
    action='store_true',
    help='Put MCU into bootloader mode')

group.add_argument(
    '--enterapp', 
    action='store_true',
    help='Put MCU into app mode')

args, unknown = parser.parse_known_args()

if args.enterboot:
    log.log(level = log.INFO, message = f"Calling enterboot script with {unknown} arguments")
    enterboot.main(unknown)

elif args.enterapp:
    log.log(level = log.INFO, message = f"Calling enterapp script with {unknown} arguments")
    enterapp.main(unknown)