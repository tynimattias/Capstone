
import serial
from time import monotonic
import sys

class BN880:

    def __init__(self, i2cdata, i2cclk, clkrate, info_tag, serialport) -> None:
        self.i2cdata = i2cdata
        self.i2cclk = i2cclk
        self.NMEA_buff = []
        self.lat_in_degrees = 0
        self.long_in_degrees = 0
        self.clkrate = clkrate
        self.info_tag = info_tag
        self.serialport = serialport
        self.ser = serial.Serial(self.serialport)
        self.gpgga_info = info_tag
        self.GPGGA_buffer = 0

    def magneometer_setup(self):
        pass

    def gps_info(self):
        nmea_time = []
        nmea_latitude = []
        nmea_longitude = []
        nmea_time = self.NMEA_buff[0]
        nmea_longitude = self.NMEA_buff[1]
        nmea_latitude = self.NMEA_buff[3]
        
        self.lat = float(nmea_latitude)
        self.longi = float(nmea_longitude)

        self.lat_in_degrees = BN880.convert_to_degrees(self,self.lat)
        self.long_in_degrees = BN880.convert_to_degrees(self,self.longi)
        
    
    def convert_to_degrees(self,value):
        decimal_value = value/100.00
        degrees = int(decimal_value)
        mm_mmmm = (decimal_value - int(decimal_value))/0.6
        position = degrees + mm_mmmm
        position = "%.4f" %(position)
        return position

   
    def get_position(self):
        data_avaliable = -1   
        timeout_initial = monotonic()
        while(data_avaliable==-1):
            if(timeout_initial+2< monotonic()):
                raise TimeoutError
                
            recieved_data = (str)(self.ser.readline())
            data_avaliable = recieved_data.find(self.gpgga_info)
        if (data_avaliable>0):
            self.GPGGA_buffer = recieved_data.split("$GNGGA,",1)[1]
            self.NMEA_buff = (self.GPGGA_buffer.split(','))
            BN880.gps_info(self)
        else:
            print('No gppa found')
        return self.lat_in_degrees, self.long_in_degrees

if __name__ == "__main__":
    gps = BN880(0,0,9600, "$GNGGA", "/dev/serial0")

    lat, longi= gps.get_position()
    
    print(f"Latitude is {latn}, longitude is {longin}")
