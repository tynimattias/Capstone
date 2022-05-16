import numpy as np
import time
from time import sleep
import RPi.GPIO as gpio
import os




class Ultrasonic_Sensor:
    
    
    
    
    def __init__(self, echo, trigger, average_terms):
        self.echo = echo
        self.trigger = trigger
        self.edge_count = 0
        self.timer_value1 = 0
        self.timer_value2  = 0
        self.average_terms = average_terms
    
    def setup(self):
        print(f"setup ultrasonic sensor on echo {self.echo}")
        if(gpio.getmode()== None):
            gpio.setmode(gpio.BCM)
            print("set mode to BOARD")
            
        gpio.setup(self.echo, gpio.IN)
        gpio.setup(self.trigger, gpio.OUT)
        print(f"Trigger setup on echo {self.trigger}")
    
    def measure(self):
        
        average_array = np.zeros(self.average_terms)
        #print(f"Measure {self.echo}")
        for i in range(len(average_array)):
            Ultrasonic_Sensor.pulse(self)
            
            initial_timeout_time = time.time()
            while(gpio.input(self.echo)==0):
                self.timer_value2 = time.time()
                #print("hit")
                if(initial_timeout_time+1<=time.time()):
                    print(f"timer for echo on echo {self.echo} timed out!")
                    
                    break
                    

            initial_timeout_time = time.time()
            while(gpio.input(self.echo)==1):
                #print(gpio.input(self.echo))
                #print(self.echo)
                self.timer_value1 = time.time()
                if(initial_timeout_time+1<=time.time()):
                    print(f"timer for echo on echo {self.echo} timed out!")
                    
                    
                    break
                    
                    
           
            
            
            pulse = (self.timer_value1 - self.timer_value2)
            
            sleep(0.03)
            distance = (0.5)*(pulse)*343
            
            average_array[i] = distance
            
        #print(" End Measure")
        
        
        return sum(average_array)/len(average_array) *100
        
    
    def pulse(self):
        
        gpio.output(self.trigger, gpio.HIGH)
        sleep(15E-6)
        gpio.output(self.trigger, gpio.LOW)
        #print("pulse")
    
    
    
    def __del__(self):
        print(F"Sensor on echo{self.echo} was removed!")
        
