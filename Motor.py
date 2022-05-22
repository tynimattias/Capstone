
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
            gpio.setmode(gpio.BCM)
            print("set mode to BOARD")
        
        motor_inputs = [self.in1,self.in2,self.in3,self.in4]
        
        gpio.setup(motor_inputs,gpio.OUT)
        gpio.output(motor_inputs, gpio.LOW)
        
    def Forward(self, tm = 0.75):
        print('Forward')
        gpio.output(self.in1,gpio.HIGH)
        gpio.output(self.in2,gpio.LOW)
        gpio.output(self.in3,gpio.HIGH)
        gpio.output(self.in4,gpio.LOW)
        time.sleep(tm)
        print('Forward Complete')

    def Backward(self, tm = 0.75):
        print("Backward")
        gpio.output(self.in1,gpio.LOW)
        gpio.output(self.in2,gpio.HIGH)
        gpio.output(self.in3,gpio.LOW)
        gpio.output(self.in4,gpio.HIGH)
        time.sleep(tm)
        print('Backward Complete')
        
    def Left(self, tm = 2.5):
        print("Turning Left")
        gpio.output(self.in1,gpio.HIGH)
        gpio.output(self.in2,gpio.LOW)
        gpio.output(self.in3,gpio.LOW)
        gpio.output(self.in4,gpio.HIGH)
        print('Left Complete')
        time.sleep(tm)
        

    def Right(self, tm = 2.4):
        print("Turing Right")
        gpio.output(self.in1,gpio.LOW)
        gpio.output(self.in2,gpio.HIGH)
        gpio.output(self.in3,gpio.HIGH)
        gpio.output(self.in4,gpio.LOW)
        print('Right Complete')
        time.sleep(tm)
    def Stop(self):
        gpio.output(self.in1,gpio.LOW)
        gpio.output(self.in2,gpio.LOW)
        gpio.output(self.in3,gpio.LOW)
        gpio.output(self.in4,gpio.LOW)
        print("Stop?")


if __name__ == "__main__":
    
    while(1):
        motor = Motor(12, 16, 21, 20)
        motor.setup()
        
        direction = int(input('0/1/2/3/4'))
        ti = float(input('Calibration time'))
        
        if(direction==0):
                
            motor.Forward(tm = ti)
            motor.Stop()
            
        elif(direction==1):
            
            motor.Right(tm = ti)
            #motor.Forward()
            motor.Stop()
            
            
        elif(direction==2):
            
            motor.Backward(tm = ti)
            motor.Stop()
            
        elif(direction==3):
            
            motor.Left(tm = ti)
            motor.Stop()
            
        elif(direction==4):
            motor.Stop()
        elif(direction==6):
            exit()
            
        else:
            print('No direction recieved, Error?')
        
        direction = -1
                    

