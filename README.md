### Eastern Washington Universty: Electrical Engineering Capstone 2022
Raspberry Pi4 Code for Heat-Seeking Car

This repository contains all the code and schematics on the Raspberry Pi for the Heat-Seeking Car capstone project completed in June 2022.

This code is to be used in conjuction with Amelya Avdeyev's code found [here](https://www.github.com/aavdeyev1/Heat-Seeking-Car)

### Using this code

To use this code, upload this code to the Raspberry Pi 4 and run Main.py. I would advise running the Pi in headless mode and talking to it over ssh so that the Car is wireless. 

### Sensor Setup

#### Ultrasonic Sensors

This code as it stands uses 4x ultrasonic sensors. The code can be adjusted to accomadate more sensors by creating a new Ultrasonic Sensor object from the Ultrasonic Sensor Class in Ultrasonic.py.

As it stands right now, all ultrasonic sensors share the same 5v rail and ground. 

The following pin definitions are based off of BCM (Gpio) Pin numbers, NOT BOARD  
North Ultrasonic Sensor: Trigger = 6; Echo = 13  
East Ultrasonic Sensor: Trigger = 24; Echo = 23  
South Ultrasonic Sensor: Trigger = 11; Echo = 10  
West Ultrasonic Sensor: Trigger = 26; Echo = 19  

#### Mlx90640 with Adafruit Breakout Board

Make sure that I2C is setup on the Raspberry Pi

Connect 3v3 pin to the 3v3 pin on the Rpi4. Connect gnd to the ground pin on the Rpi4. connect SDA (Serial Data) to the SDA pin on the Pi which is board pin number 3. Connect SCL (Serial Clock) to board pin 5. 

#### BN880

Make sure that UART connection is setup on the Raspberry Pi. 

Connect 5v to 5v rail. Connect Ground to Ground. Connect the BN880 Rx pin to the Tx pin on the Raspberry pi, (Board pin 8). Connect BN880 Tx pin to Rx on Raspberry Pi, (Board Pin 10)


### Questions?
Contact me at tynimattias@gmail.com
