
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
        
    def Forward(self, time = 0.88):
        print('Forward')
        gpio.output(self.in1,gpio.HIGH)
        gpio.output(self.in2,gpio.LOW)
        gpio.output(self.in3,gpio.HIGH)
        gpio.output(self.in4,gpio.LOW)
        time.sleep(time)
        print('Forward Complete')

    def Backward(self, time = 0.98):
        print("Backward")
        gpio.output(in1,gpio.LOW)
        gpio.output(in2,gpio.HIGH)
        gpio.output(in3,gpio.LOW)
        gpio.output(in4,gpio.HIGH)
        time.sleep(time)
        print('Backward Complete')
        
    def Left(self, time = 0.85, fwd_time = 0.88):
        print("Turning Left")
        gpio.output(in1,gpio.HIGH)
        gpio.output(in2,gpio.LOW)
        gpio.output(in3,gpio.LOW)
        gpio.output(in4,gpio.HIGH)
        print('Left Complete')
        time.sleep(time)
        Motor.Forward(self, time = fwd_time)

    def Right(self, time = 0.80, fwd_time = 0.88):
        print("Turing Right")
        gpio.output(self.in1,gpio.LOW)
        gpio.output(self.in2,gpio.HIGH)
        gpio.output(self.in3,gpio.HIGH)
        gpio.output(self.in4,gpio.LOW)
        print('Right Complete')
        time.sleep(time)
        Motor.Forward(self, time = fwd_time)




