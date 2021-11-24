import smbus
import time
bus = smbus.SMBus(1)
address = 0x5a

def temperature():
        bear = bus.read_byte_data(address, 0x07)
        #bear = (bear >> 1)
        return bear

def readTemp():
        temp = temperature()
        #temp *= 0.02
        temp -= 273
        return temp


#print(readTemp())
print(bus.read_byte_data(address, 0x06))
#print(bus.read_word_data(address, 0x24))

while False:
        bearing = bearing3599()     #this returns the value to 1 decimal place in degrees. 
        bear255 = bearing255()      #this returns the value as a byte between 0 and 255. 
        print(bearing)
        print(bear255)
        time.sleep(1)