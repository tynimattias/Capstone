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
            print("set mode to BCM")
            
        gpio.setup(self.echo, gpio.IN)
        gpio.setup(self.trigger, gpio.OUT)
        
        print(f"Trigger setup on echo {self.trigger}")
    
    def measure(self):
        
        average_array = np.zeros(self.average_terms)
        #print(f"Measure {self.echo}")
        for i in range(len(average_array)):
            Ultrasonic_Sensor.pulse(self)
            
            initial_timeout_time = time.monotonic()
            while(gpio.input(self.echo)==0):
                self.timer_value2 = time.monotonic()
                #print("hit")
                if(initial_timeout_time+2<=time.monotonic()):
                    print(f"initial timer for echo on echo {self.echo} timed out!")
                    
                    break
                    

            initial_timeout_time = time.monotonic()
            while(gpio.input(self.echo)==1):
                #print(gpio.input(self.echo))
                #print(self.echo)
                self.timer_value1 = time.monotonic()
                if(initial_timeout_time+1<=time.monotonic()):
                   print(f"measure timer for echo on echo {self.echo} timed out!")
                   break
                    
                    
           
            
            
            pulse = (self.timer_value1 - self.timer_value2)
            
            sleep(0.03)
            distance = (0.5)*(pulse)*343
            
            average_array[i] = distance
            
        #print(" End Measure")
        
        
        return sum(average_array)/len(average_array) *100
        
    
    def pulse(self):
        gpio.output(self.trigger, gpio.LOW)
        sleep(15E-6)
        gpio.output(self.trigger, gpio.HIGH)
        sleep(15E-6)
        gpio.output(self.trigger, gpio.LOW)
        
    
    
    
    def __del__(self):
        print(F"Sensor on echo{self.echo} was removed!")

     

if __name__ == "__main__":
    sensors = []
    sensors.append(Ultrasonic_Sensor(13,6,1)) #North
    sensors.append(Ultrasonic_Sensor(23,24,1)) #East
    sensors.append(Ultrasonic_Sensor(10,11,1)) #south
    sensors.append(Ultrasonic_Sensor(19,26,1)) #West
    measurements = np.zeros(4)
    previuous_measure = measurements
    for i in range(len(sensors)):
        sensors[i].setup()


    while(1):
        
        #For every sensor in the sensor object list,
        #measure the distance from that sensor and 
        #store into observation vector
        for i in range(len(sensors)):
            
            
            measurements[i] = sensors[i].measure()
            if(np.abs(previuous_measure[i]-measurements[i])>200):
                while(np.abs(previuous_measure[i]-measurements[i])>400):
                    measurements[i] = sensors[i].measure()
                    previuous_measure[i] = 400
        previuous_measure = measurements

        print(f"Forward: {measurements[0]}\nRight: {measurements[1]}\nBack: {measurements[2]}\nLeft: {measurements[3]}")
        print("__________________________________")
        