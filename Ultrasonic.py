import numpy as np
import time
from time import sleep
import RPi.GPIO as gpio




class Ultrasonic_Sensor:
    
    
    
    
    def __init__(self, pin, trigger):
        self.pin = pin
        self.trigger = trigger
        self.edge_count = 0
        self.timer_value1 = 0
        self.timer_value2  = 0
    
    def setup(self):
        print(f"setup ultrasonic sensor on pin {self.pin}")
        if(gpio.getmode()== None):
            gpio.setmode(gpio.BOARD)
            print("set mode to BOARD")
            
        gpio.setup(self.pin, gpio.IN)
        gpio.setup(self.trigger, gpio.OUT)
        print(f"Trigger setup on pin {self.trigger}")
    
    def measure(self):
        
        average_array = np.zeros(5)
        
        for i in range(len(average_array)):
            Ultrasonic_Sensor.pulse(self)
            while(gpio.input(self.pin)==0):
                self.timer_value2 = time.time()
            while(gpio.input(self.pin)==1):
                self.timer_value1 = time.time()  
            self.timer_value_1 = time.time()
            
            pulse = (self.timer_value1 - self.timer_value2)
            
            sleep(0.03)
            distance = (0.5)*(pulse)*343
            
            average_array[i] = distance
            
        
        
        
        return sum(average_array)/len(average_array) *100
        
    
    def pulse(self):
        
        gpio.output(self.trigger, gpio.HIGH)
        sleep(15E-6)
        gpio.output(self.trigger, gpio.LOW)
        
    
    
    
    def __del__(self):
        print(F"Sensor on pin{self.pin} was removed!")
        