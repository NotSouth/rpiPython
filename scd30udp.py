
from scd30_i2c import SCD30
import socket
import json
import types
import time


serverAddressPort = ("255.255.255.255", 10010)


def sendData(m):
    # This a fake class, that's just simple to use.
    # Attributes are added as soon as you declare them.
    x = types.SimpleNamespace()
    x.ID = 0
    x.CO2 = round(m[0],2)
    x.Temperature = round(m[1],2)
    x.Humidity = round(m[2],2)
    x.TimeStamp = "0001-01-01T00:00:00"

    #print("Temperature:", x.Temperature)
    #print("CO2:", x.CO2)
    #print("Humidity:", x.Humidity)

    print(f"CO2: {x.CO2} ppm, temp: {x.Temperature} 'C, rh: {x.Humidity}%")

    # It doesn't know how to serialize it, so the default stuff has be included. "It just works (TM)"
    json_string = json.dumps(x, default=lambda o: o.__dict__)
    bytesToSend = str.encode(json_string)


    # Create a UDP socket at client side
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # Broadcast is disabled by default. Need to allow manually.
    UDPClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # Send to server using created UDP socket
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)


scd30 = SCD30()
#scd30.soft_reset()
scd30.set_measurement_interval(2)
scd30.start_periodic_measurement(0) # Ambient pressure compensation
scd30.set_temperature_offset(2.8)
scd30.set_auto_self_calibration(True)
print(scd30.get_firmware_version())

time.sleep(2)

try:
    while True:
        if scd30.get_data_ready():
            m = scd30.read_measurement()
            if m is not None:
                #print(f"CO2: {m[0]:.2f}ppm, temp: {m[1]:.2f}'C, rh: {m[2]:.2f}%")
                sendData(m)
            time.sleep(2)
        else:
            time.sleep(0.2)
except KeyboardInterrupt:
    scd30.stop_periodic_measurement()
