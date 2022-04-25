from Ultrasonic import Ultrasonic_Sensor
import threading
from time import sleep
import numpy as np

sensors = []
sensors.append(Ultrasonic_Sensor(18,7))
sensors.append(Ultrasonic_Sensor(22,11))
sensors.append(Ultrasonic_Sensor(24,13))
sensors.append(Ultrasonic_Sensor(26,15))


for i in range(len(sensors)):
    sensors[i].setup()
    
    


Observation_Vector = np.zeros(1000)

def ultrasonic_sensor():
    while(1):
        
        for i in range(len(sensors)):
            
            Observation_Vector[i] = sensors[i].measure()
            if(Observation_Vector[i]>=400):
                Observation_Vector[i] = 400
            
            
            
        print(f"Sensor 1: {Observation_Vector[0]}\nSensor 2: {Observation_Vector[1]}\nSensor 3: {Observation_Vector[2]}\nSensor 4: {Observation_Vector[3]}")
        print("__________________________________")

def thermal_camera():
    pass
def motor_control():
    pass



t1 = threading.Thread(target = ultrasonic_sensor)
t2 = threading.Thread(target = thermal_camera)
t3 = threading.Thread(target = motor_control)

t1.start()



                                    




