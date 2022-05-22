from BN880 import BN880
from Ultrasonic import Ultrasonic_Sensor
import RPi.GPIO as gpio
import threading
import Motor
from time import sleep
import numpy as np
import adafruit_mlx90640
import busio

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

#Global Variable for under voltage detection

under_voltage = 0

#Global variable for direction, intialized to -1(0 is reserved for Forward)
direction = -1
request = 0

lock = threading.Lock()


#Create instance of class Mqtt client with id Rp4
client = mqtt.Client(client_id="Rp4")

#Subscribes to Observation and Direction topics on connection
def on_connect(client, userdata, flags, rc):
    #print(f"Connected with code {rc}")
    
    
    client.subscribe("HeatSeekingCar/Direction")
    client.subscribe("HeatSeekingCar/Request")

#When data is recieved, check for direction topic and assign as the direction
def on_message(client, userdata, msg):
    #print(f"{msg.topic}: {msg.payload}")
    global direction, request
    
    try:
        if msg.topic == "HeatSeekingCar/Direction":
            direction = int(msg.payload)
        if msg.topic == "HeatSeekingCar/Request":
            request = int(msg.payload)
            #print(f"Request was {request}")
    except ValueError:
        pass


client.on_connect = on_connect
client.on_message = on_message

broker = "test.mosquitto.org"

#Connecting to mosquitto for broker with keep alive of 10min
client.connect(broker, 1883, keepalive = 600)

#Begin mqtt client loop
client.loop_start()


#Sensor objects will be stored in an array(list) [N,W,S,E]
#Is adaptable to include more sensors if desired
#Just add sensors.append(Ultrasonic_Sensor(ECHO, TRIGGER, Averaging_Terms)


#----Change pins to accomadate gps**********************************************
sensors = []
#Echo Blue, Trigger Yellow
sensors.append(Ultrasonic_Sensor(13,6,5)) #North
sensors.append(Ultrasonic_Sensor(23,24,5)) #East
sensors.append(Ultrasonic_Sensor(10,11,5)) #south
sensors.append(Ultrasonic_Sensor(19,26,5)) #West

#MLX90640 Initiation


i2c = busio.I2C(3, 2, frequency=800000)

mlx = adafruit_mlx90640.MLX90640(i2c)
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_4_HZ

#Create an empty frame which will be the size of the camera (24x32)

frame = np.zeros(768)

#Create a Motor Object with parameters (In1, In2, In3, In4)
motor = Motor.Motor(12, 16, 21, 20)

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
    global Observation_Vector
    
    while(1):
        global under_voltage
        previuous_measure = np.zeros(4)
        if(under_voltage):
            break
        #For every sensor in the sensor object list,
        #measure the distance from that sensor and 
        #store into observation vector
        lock.acquire()
        for i in range(len(sensors)):
            Observation_Vector[i] = sensors[i].measure()
            if(np.abs(previuous_measure[i]-Observation_Vector[i])>200):
                while(np.abs(previuous_measure[i]-Observation_Vector[i])>400):
                    Observation_Vector[i] = sensors[i].measure()
                    previuous_measure[i] = 400
            previuous_measure = Observation_Vector[0:4]
            
        
        lock.release()
        #print(f'Board mode is {gpio.getmode()}')        
        #print(f"Forward: {Observation_Vector[0]}\nRight: {Observation_Vector[1]}\nBack: {Observation_Vector[2]}\nLeft: {Observation_Vector[3]}")
        #print("__________________________________")
            
            
        
#Task 2: Thermal Camera
#Simple task using Adafruit's MLX90640 Library
#mlx.getFrame is used to get a frame from the thermal camera
#Sometimes values errors WILL happen, just try again
def thermal_camera():
    while(1):
        global Observation_Vector
        global under_voltage
        if(under_voltage):
            break
        try:
            mlx.getFrame(frame)
        except RuntimeError:
            print("Mlx frame aquire fail")
            continue
        #Store values into observation vector
        Observation_Vector[4:len(frame)+4] = frame
        
        sum_frame = np.sum(frame)

        frame_average = sum_frame/len(frame)

        higher_than_average_array = np.zeros(len(frame))

        for i in range(len(frame)):
            if(frame[i]>=frame_average):
                higher_than_average_array[i] = 1
            else:
                higher_than_average_array[i] = 0

        percentage = np.sum(higher_than_average_array)/len(frame)

        print(f'Percentage is {percentage*100}%')

        for h in range(24):
            for w in range(32):
                t = frame[h * 32 + w]
                
                c = "&"
                # pylint: disable=multiple-statements
                if t < 20:
                    c = " "
                elif t < 23:
                    c = "."
                elif t < 25:
                    c = "-"
                elif t < 27:
                    c = "*"
                elif t < 29:
                    c = "+"
                elif t < 31:
                    c = "x"
                elif t < 33:
                    c = "%"
                elif t < 35:
                    c = "#"
                elif t < 37:
                    c = "X"
                # pylint: enable=multiple-statements
                print(c, end="")
            print()
        print()
        
    
    


#Task 3: Motor Control
def motor_control():
    global direction
    while(1):
        #Wait until direction command is recieved.
        #Once a command is recieved [0,1,2,3,4], if statement becomes true and car will move
        #Reset to -1 so we don't get continuous travel
        #(example, direction stays at 2, will continue to make trigger motor because the condition remains true)
        
        global under_voltage
        if(under_voltage):
            break
       
        
            
        #print(direction)
        if(direction+1):
            if(direction==0):
                
                motor.Forward()
                motor.Stop()
            
            elif(direction==1):
                
                motor.Right()
                motor.Forward()
                motor.Stop()
                
                
            elif(direction==2):
                
                motor.Backward()
                motor.Stop()
                
            elif(direction==3):
                
                motor.Left()
                motor.Forward()
                motor.Stop()
                
            elif(direction==4):
                motor.Stop()
                
            else:
                pass
                #print('No direction recieved, Error?')
            
            direction = -1
        else:
            #if no command is avaliable, sleep for 0.5 sec to allow other tasks to work
            sleep(0.5)
                

def transmitter():
    global request
    global Observation_Vector
    global under_voltage
    while(1):
        #print(Observation_Vector)
        if(request):
            #print("Data Requested")
            publish.single("HeatSeekingCar/Observation_Vector", str(Observation_Vector), hostname = broker)
            
            request = 0

        if(under_voltage):

            #print("Under_voltage: Car shutting off")
            publish.single("HeatSeekingCar/Undervoltage", str(1), hostname = broker)
            
            





def low_voltage_detection():
    global under_voltage
    gpio.setup(8, gpio.IN)
    while(True): 
        under_voltage = gpio.input(8)


    
def gps():
    global Observation_Vector    
    gps = BN880(0,0,9600, "$GNGGA", "/dev/serial0")
    while(1):
        try:
            lat, longi= gps.get_position()
            Observation_Vector[-2] = lat; Observation_Vector[-1] = longi

        except TimeoutError:
            print('GPS Timed Out!')
            Observation_Vector[-2] = 3; Observation_Vector[-1] = 2

#Threading declarations
t1 = threading.Thread(target = ultrasonic_sensor)
t2 = threading.Thread(target = thermal_camera)
t3 = threading.Thread(target = motor_control)
t4 = threading.Thread(target = transmitter)
t5 = threading.Thread(target = low_voltage_detection)
t6 = threading.Thread(target= gps)

t1.start()
t2.start()
t3.start()
t4.start()
#t5.start()
t6.start()
