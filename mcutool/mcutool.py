from tools.argparse_handler import CustomArgumentParser
import os
import sys
from tools import enterboot, enterapp
from tools.logger import logger

def main(args=None):
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

    parser = CustomArgumentParser(
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

    if args == None:
        args = sys.argv[1:]
    scriptargs, unknown = parser.parse_known_args(args)
    if unknown:
        log.log(level = log.INFO, message = f"mcutool unrecognized args: {unknown}")
    
    if scriptargs.enterboot:
        log.log(level = log.INFO, message = f"Calling enterboot script with {unknown} arguments")
        try:
            enterboot.main(unknown)
        except Exception as e:
            log.log(level = log.CRITICAL, message = f"enterboot script was not able to be completed: {e}")
            sys.exit(1)

    elif scriptargs.enterapp:
        log.log(level = log.INFO, message = f"Calling enterapp script with {unknown} arguments")
        try:
            enterapp.main(unknown)
        except Exception as e:
            log.log(level = log.CRITICAL, message = f"enterapp script was not able to be completed: {e}")
            sys.exit(1)

    log.log(level = log.INFO, message = "mcutool completed as expected")
    sys.exit(0)

if __name__=='__main__':
    main()