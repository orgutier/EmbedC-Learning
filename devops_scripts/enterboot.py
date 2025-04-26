import RPi.GPIO as gpio
from time import sleep

reset = 27
boot = 4

gpio.setmode(gpio.BCM)
gpio.setup(reset, gpio.OUT)
gpio.setup(boot, gpio.OUT)

# Booot and reset pins preconditions
gpio.output(reset, gpio.LOW)
gpio.output(boot, gpio.LOW)

sleep(1)
gpio.output(boot, gpio.HIGH)

sleep(1)
gpio.output(reset, gpio.HIGH)

sleep(1)
gpio.output(reset, gpio.LOW)
# Keep boot pin pressed during flash
# gpio.cleanup()
