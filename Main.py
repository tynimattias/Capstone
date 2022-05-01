from Ultrasonic import Ultrasonic_Sensor
import threading
import Motor
from time import sleep
import numpy as np
import adafruit_mlx90640
import busio
import board
import paho.mqtt.client as mqtt


#Global variable for direction, intialized to -1(0 is reserved for Forward)
direction = -1


#Create instance of class Mqtt client with id Rp4
client = mqtt.Client(client_id="Rp4")

#Subscribes to Observation and Direction topics on connection
def on_connect(client, userdata, flags, rc):
    print(f"Connected with code {rc}")

    client.subscribe("HeetSeekingCar/Observation")
    client.subscribe("HeatSeekingCar/Direction")

#When data is recieved, check for direction topic and assign as the direction
def on_message(client, userdata, msg):
    print(f"{msg.topic}: {msg.payload}")
    global direction

    if msg.topic == "Direction":
        direction = msg.payload



client.on_connect = on_connect
client.on_message = on_message

#Connecting to mosquitto for broker with keep alive of 10min
client.connect("test.mosquitto.org", 1883, keepalive = 600)

#Begin mqtt client loop
client.loop_start()


#Sensor objects will be stored in an array(list) [N,W,S,E]
#Is adaptable to include more sensors if desired
#Just add sensors.append(Ultrasonic_Sensor(ECHO, TRIGGER, Averaging_Terms)

sensors = []
sensors.append(Ultrasonic_Sensor(33,31,1)) #North
sensors.append(Ultrasonic_Sensor(35,37,1)) #West
sensors.append(Ultrasonic_Sensor(19,21,1)) #south
sensors.append(Ultrasonic_Sensor(10,12,1)) #East


#MLX90640 Initiation
i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)


mlx = adafruit_mlx90640.MLX90640(i2c)
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_4_HZ

#Create an empty frame which will be the size of the camera (24x32)

frame = np.zeros(768)

#Create a Motor Object with parameters (In1, In2, In3, In4)
motor = Motor.Motor(16, 18, 22, 24)

#Will setup appropiate pins to be 
motor.setup()


#For loop sets up appropriate pins for input and output
#Echo pins will be set up for input
#Trigger Pins are setup for output
for i in range(len(sensors)):
    sensors[i].setup()
    
#Create an array of zeros for the observation vector
Observation_Vector = np.zeros(774)

#Task 1: Ultrasonic Sensors
def ultrasonic_sensor():
    
    while(1):
        
        #For every sensor in the sensor object list,
        #measure the distance from that sensor and 
        #store into observation vector
        for i in range(len(sensors)):
            
            Observation_Vector[i] = sensors[i].measure()
            
            #Sensors freak out for large distance and are unreliable
            #Best if that a value is over the manufacturer rating
            #Set to the manufacturer rating and assume it's safe to go

            if(Observation_Vector[i]>=400):
                Observation_Vector[i] = 400
        
        print(f"Sensor 1: {Observation_Vector[0]}\nSensor 2: {Observation_Vector[1]}\nSensor 3: {Observation_Vector[2]}\nSensor 4: {Observation_Vector[3]}")
        print("__________________________________")
            
            
        
#Task 2: Thermal Camera
#Simple task using Adafruit's MLX90640 Library
#mlx.getFrame is used to get a frame from the thermal camera
#Sometimes values errors WILL happen, just try again
def thermal_camera():
    while(1):
        try:
            mlx.getFrame(frame)
        except ValueError:
            continue
        #Store values into observation vector
        Observation_Vector[4:len(frame)+4] = frame
        #print(Observation_Vector)


#Task 3: Motor Control
def motor_control():
    while(1):
        #Wait until direction command is recieved.
        #Once a command is recieved [0,1,2,3,4], if statement becomes true and car will move
        #Reset to -1 so we don't get continuous travel
        #(example, direction stays at 2, will continue to make trigger motor because the condition remains true)
        if(direction-1):
            if(direction==0):
                motor.Forward()
                direction = -1
            elif(direction==1):
                motor.Right()
                direction = -1
            elif(direction==2):
                motor.Backward()
                direction = -1
            elif(direction==3):
                motor.Left()
                direction = -1
            else:
                print('No direction recieved, Error?')
        else:
            #if no command is avaliable, sleep for 0.5 sec to allow other tasks to work
            sleep(0.5)



#Threading declarations
t1 = threading.Thread(target = ultrasonic_sensor)
t2 = threading.Thread(target = thermal_camera)
t3 = threading.Thread(target = motor_control)

t1.start()
t2.start()
t3.start()