# EENG 490A
# Motor Control Program
# Artyom Gurdyumov

import RPi.GPIO as GPIO
import time

# Driver Board pins to Raspberry Pi 4 pins
in1 = 16
in2 = 20
in3 = 19
in4 = 26

# Delay Times
x = 0.88 # Forward 20cm
x1 = 0.98 # Backward 20cm
x2 = 0.85 # turining right 
x3 = 0.8 # turing left 

# setup GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)



while(1):
    direction = int(input("Enter direction command: "))
    if direction == 0:  # going forward 20cm
        print("Forward")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
        time.sleep(x)
        direction = -1
    elif direction == 1:  # Rotate Right 90 degrees, move forward 20cm
        print("Turing Right")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
        time.sleep(x2)
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
        time.sleep(x)
        direction = -1
    elif direction == 2:  # going backward 20cm
        print("Backward")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)
        time.sleep(x1)
        direction = -1
    elif direction == 3:  # Rotate left 90 Degrees, move forward 20cm
        print("Turning Left")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)
        time.sleep(x3)
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
        time.sleep(x)
        direction = -1
    elif direction == 4:  # stop car
        print("Stop")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)
        direction = -1
    elif direction ==5:
        break

GPIO.cleanup()
