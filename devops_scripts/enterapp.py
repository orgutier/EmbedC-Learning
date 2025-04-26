import RPi.GPIO as gpio
from time import sleep
from logger import logger
import os
import sys

log = logger()
notifyname = None
notifyid = None
try:
    log.appname = os.path.basename(__file__)
except Exception as e:
    # No problem, use default
    log.appname = "enterapp"
    notifyname = e
try:
    log.taskid = int(os.getpid())
except Exception as e:
    # No problem, use default
    log.taskid = 1111
    notifyid = e

if notifyname:
    log.log( level = log.WARN, message = "appname was not defined, using default")
    log.log( level = log.WARN, message = f"Error: {notifyname}")
if notifyid:
    log.log(level = log.WARN, message = "taskid was not defined, using default")
    log.log( level = log.WARN, message = f"Error: {notifyid}")

log.log(level = log.DEBUG, message = f"appname|taskid -- {log.appname}|{log.taskid}",)
log.log(level = log.INFO, message = "Starting app reset")

reset = 27
boot = 4
# ------------ DEBUG -------------
log.log(level = log.DEBUG, message = f"Reset pin: {reset}")
log.log(level = log.DEBUG, message = f"Boot pin: {boot}")


try:
    gpio.setmode(gpio.BCM)
    gpio.setup(reset, gpio.OUT)
    gpio.setup(boot, gpio.OUT)
except Exception as e:
    log.log(level = log.CRITICAL, message = "Unable to set reset/boot pins: {e}")
    sys.exit(1)

try:
    # Booot and reset pins preconditions
    gpio.output(reset, gpio.LOW)
    gpio.output(boot, gpio.LOW)

    sleep(1)
    gpio.output(reset, gpio.HIGH)

    sleep(1)
    gpio.output(reset, gpio.LOW)
    # Keep boot pin pressed during flash
    # gpio.cleanup()
except Exception as e:
    log.log(level = log.CRITICAL, message = "Unable to set gpio transitions: {e}")
    log.log( level = log.WARN, message = f"Error: {e}")
    sys.exit(1)

log.log(level = log.INFO, message = "Completed app reset as expected")

sys.exit(0)


