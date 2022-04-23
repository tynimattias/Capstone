import numpy as np
import time
from time import sleep
import RPi.GPIO as gpio




class Ultrasonic_Sensor:
    
    
    edge_count = 0
    time_measure0 = 0
    time_measure1 = 0
    timer_value1 = 0
    timer_value2  = 0
    
    def __init__(self, pin, trigger):
        self.pin = pin
        self.trigger = trigger
        
    
    def setup(self):
        print(f"setup ultrasonic sensor on pin {self.pin}")
        if(gpio.getmode()== None):
            gpio.setmode(gpio.BOARD)
            print("set mode to BOARD")
            
        gpio.setup(self.pin, gpio.IN)
        gpio.setup(self.trigger, gpio.OUT)
        print(f"Trigger setup on pin {self.trigger}")
    
    def measure(self):
        gpio.add_event_detect(self.pin, gpio.BOTH)
        gpio.add_event_callback(self.pin, Ultrasonic_Sensor.interrupt_handler)
        Ultrasonic_Sensor.pulse(self)
        
        
        pulse = (Ultrasonic_Sensor.timer_value2 - Ultrasonic_Sensor.timer_value1)
        
        print(f"Pulse is {pulse}")
        distance = (0.5)*(pulse)*343
        gpio.remove_event_detect(self.pin)
        return distance
        
    
    def pulse(self):
        
        gpio.output(self.trigger, gpio.HIGH)
        sleep(10E-6)
        gpio.output(self.trigger, gpio.LOW)
        
    def interrupt_handler(self):
        
        if(Ultrasonic_Sensor.edge_count == 0):
            Ultrasonic_Sensor.timer_value1 = time.time()*1000
            edge_count +=1
        if(Ultrasonic_Sensor.edge_count == 1):
            Ultrasonic_Sensor.timer_value2 = time.time()*1000
            edge_count =0
    
    
    def __del__(self):
        print(F"Sensor on pin{self.pin} was removed!")
        