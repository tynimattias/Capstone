
import RPi.GPIO as gpio
import time

class Motor():
    
    def __init__(self, in1, in2, in3, in4):
        self.in1 = in1
        self.in2 = in2
        self.in3 = in3
        self.in4 = in4
        
        
    def setup(self):
        if(gpio.getmode()== None):
            gpio.setmode(gpio.BOARD)
            print("set mode to BOARD")
        
        motor_inputs = [self.in1,self.in2,self.in3,self.in4]
        
        gpio.setup(motor_inputs,gpio.OUT)
        gpio.output(motor_inputs, gpio.LOW)
        
    def Forward(self, tm = 0.88):
        print('Forward')
        gpio.output(self.in1,gpio.HIGH)
        gpio.output(self.in2,gpio.LOW)
        gpio.output(self.in3,gpio.HIGH)
        gpio.output(self.in4,gpio.LOW)
        time.sleep(tm)
        print('Forward Complete')

    def Backward(self, tm = 0.98):
        print("Backward")
        gpio.output(self.in1,gpio.LOW)
        gpio.output(self.in2,gpio.HIGH)
        gpio.output(self.in3,gpio.LOW)
        gpio.output(self.in4,gpio.HIGH)
        time.sleep(tm)
        print('Backward Complete')
        
    def Left(self, tm = 0.85, fwd_time = 0.88):
        print("Turning Left")
        gpio.output(self.in1,gpio.HIGH)
        gpio.output(self.in2,gpio.LOW)
        gpio.output(self.in3,gpio.LOW)
        gpio.output(self.in4,gpio.HIGH)
        print('Left Complete')
        time.sleep(tm)
        Motor.Forward(self, tm = fwd_time)

    def Right(self, tm = 0.80, fwd_time = 0.88):
        print("Turing Right")
        gpio.output(self.in1,gpio.LOW)
        gpio.output(self.in2,gpio.HIGH)
        gpio.output(self.in3,gpio.HIGH)
        gpio.output(self.in4,gpio.LOW)
        print('Right Complete')
        time.sleep(tm)
        Motor.Forward(self, tm = fwd_time)
    def Stop(self):
        gpio.output(self.in1,gpio.LOW)
        gpio.output(self.in2,gpio.LOW)
        gpio.output(self.in3,gpio.LOW)
        gpio.output(self.in4,gpio.LOW)
        print("Stop?")




