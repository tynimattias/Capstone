import numpy as np
import time
from time import sleep
import RPi.GPIO as gpio




class Ultrasonic_Sensor:
    
    
    
    
    def __init__(self, pin, trigger, average_terms):
        self.pin = pin
        self.trigger = trigger
        self.edge_count = 0
        self.timer_value1 = 0
        self.timer_value2  = 0
        self.average_terms = average_terms
    
    def setup(self):
        print(f"setup ultrasonic sensor on pin {self.pin}")
        if(gpio.getmode()== None):
            gpio.setmode(gpio.BOARD)
            print("set mode to BOARD")
            
        gpio.setup(self.pin, gpio.IN)
        gpio.setup(self.trigger, gpio.OUT)
        print(f"Trigger setup on pin {self.trigger}")
    
    def measure(self):
        
        average_array = np.zeros(self.average_terms)
        print(f"Measure {self.pin}")
        for i in range(len(average_array)):
            Ultrasonic_Sensor.pulse(self)
            
            initial_timeout_time = time.time()
            while(gpio.input(self.pin)==0):
                self.timer_value2 = time.time()
                if(initial_timeout_time+500<=time.time()):
                    print(f"timer for echo on pin {self.pin} timed out!")
                    break

            initial_timeout_time = time.time()
            while(gpio.input(self.pin)==1):
                self.timer_value1 = time.time()
                if(initial_timeout_time+500<=time.time()):
                    print(f"timer for echo on pin {self.pin} timed out!")
                    break
            self.timer_value_1 = time.time()
            
            
            pulse = (self.timer_value1 - self.timer_value2)
            
            sleep(0.03)
            distance = (0.5)*(pulse)*343
            
            average_array[i] = distance
            
        print(" End Measure")
        
        
        return sum(average_array)/len(average_array) *100
        
    
    def pulse(self):
        
        gpio.output(self.trigger, gpio.HIGH)
        sleep(15E-6)
        gpio.output(self.trigger, gpio.LOW)
        #print("pulse")
    
    
    
    def __del__(self):
        print(F"Sensor on pin{self.pin} was removed!")
        