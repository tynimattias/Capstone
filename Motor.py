
import RPi.GPIO as gpio

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
        
    def move(direction, time):
        
        
    