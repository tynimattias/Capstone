from time import sleep
import RPi.GPIO as gpio




gpio.setmode(gpio.BOARD)
gpio.setup(8, gpio.OUT)

while(1):
    input('toggle')
    gpio.output(8, gpio.HIGH)
    input('toggle')
    gpio.output(8, gpio.LOW)
    