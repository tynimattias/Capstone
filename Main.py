from Ultrasonic import Ultrasonic_Sensor
import threading
from time import sleep
import numpy as np

sensors = []
sensors.append(Ultrasonic_Sensor(18,16))
sensors.append(Ultrasonic_Sensor(22,16))
sensors.append(Ultrasonic_Sensor(24,16))
sensors.append(Ultrasonic_Sensor(26,16))


for i in range(len(sensors)):
    sensors[i].setup()
    
    

Observation_Vector = np.zeros(1000)

def ultrasonic_sensor():
    while(1):
        
        for i in range(len(sensors)):
            Observation_Vector[i] = sensors[i].measure()
            sleep(0.25)
            print(f"Sensor {i+1}: {Observation_Vector[i]}")
        
def thermal_camera():
    pass
def motor_control():
    pass



t1 = threading.Thread(target = ultrasonic_sensor)
t2 = threading.Thread(target = thermal_camera)
t3 = threading.Thread(target = motor_control)

t1.start()



                                    




