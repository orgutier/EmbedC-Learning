import RPi.GPIO as gpio
from time import sleep
from tools.logger import logger
import os
import sys
from tools.argparse_handler import CustomArgumentParser

def main(args=None):
    default_reset = 27
    default_boot = 4

    log = logger.logger(
        appname = os.path.basename(__file__),
        taskid = int(os.getpid())
    )

    log.log(level = log.DEBUG, message = f"appname|taskid -- {log.appname}|{log.taskid}",)

    # ------------ Define pins by parse or default
    parser = CustomArgumentParser(
        description="Enter Boot mode by setting reset and boot pins")
    parser.add_argument(
        '--resetpin', 
        type=int, 
        default=default_reset, 
        help='GPIO pin for reset')
    parser.add_argument(
        '--bootpin', 
        type=int, 
        default=default_boot, 
        help='GPIO pin for boot')

    if args == None:
        args = sys.argv[1:]
    try:
        args = parser.parse_args(args)
        reset = args.resetpin
        boot = args.bootpin
    except Exception as e:
        log.log(level = log.ERROR, message = f"Unrecognized arguments check spell: {e}")
        sys.exit(1)

    log.log(level = log.INFO, message = "Starting app reset")
    # ------------ DEBUG -------------
    log.log(level = log.DEBUG, message = f"Reset pin: {reset}")
    log.log(level = log.DEBUG, message = f"Boot pin: {boot}")


    try:
        gpio.setmode(gpio.BCM)
        gpio.setup(reset, gpio.OUT)
        gpio.setup(boot, gpio.OUT)
    except Exception as e:
        log.log(level = log.CRITICAL, message = f"Unable to set reset/boot pins: {e}")
        sys.exit(1)

    try:
        # Boot and reset pins preconditions
        gpio.output(reset, gpio.LOW)
        gpio.output(boot, gpio.LOW)

        # Keep boot high while rebooting
        sleep(1)
        gpio.output(boot, gpio.HIGH)

        sleep(1)
        gpio.output(reset, gpio.HIGH)

        sleep(1)
        gpio.output(reset, gpio.LOW)
        # Keep boot pin pressed during flash
        # gpio.cleanup()
    except Exception as e:
        log.log(level = log.CRITICAL, message = f"Unable to set gpio transitions: {e}")
        log.log( level = log.WARN, message = f"Error: {e}")
        sys.exit(1)

    log.log(level = log.INFO, message = "Completed boot reset as expected")
    log.log(level = log.INFO, message = "Intentionally left pins asserted")
        
    sys.exit(0)


if __name__ =='__main__':
    main()