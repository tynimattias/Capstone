from Ultrasonic import Ultrasonic_Sensor
import threading
from time import sleep
import numpy as np
import adafruit_mlx90640
import busio
import board

sensors = []
sensors.append(Ultrasonic_Sensor(33,31,1)) #North
sensors.append(Ultrasonic_Sensor(35,37,1)) #West
sensors.append(Ultrasonic_Sensor(19,21,1)) #south
sensors.append(Ultrasonic_Sensor(10,12,1)) #East

i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)


mlx = adafruit_mlx90640.MLX90640(i2c)
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_4_HZ

frame = np.zeros(768)


for i in range(len(sensors)):
    sensors[i].setup()
    
    


Observation_Vector = np.zeros(774)

def ultrasonic_sensor():
    
    while(1):
        
        for i in range(len(sensors)):
            
            Observation_Vector[i] = sensors[i].measure()
            
            if(Observation_Vector[i]>=400):
                Observation_Vector[i] = 400
        print(f"Sensor 1: {Observation_Vector[0]}\nSensor 2: {Observation_Vector[1]}\nSensor 3: {Observation_Vector[2]}\nSensor 4: {Observation_Vector[3]}")
        print("__________________________________")
            
            
        

def thermal_camera():
    while(1):
        try:
            mlx.getFrame(frame)
        except ValueError:
            continue
        Observation_Vector[4:len(frame)+4] = frame
        #print(Observation_Vector)
def motor_control():
    pass



t1 = threading.Thread(target = ultrasonic_sensor)
t2 = threading.Thread(target = thermal_camera)
t3 = threading.Thread(target = motor_control)

t1.start()
#t2.start()
# t3.start()



                                    




