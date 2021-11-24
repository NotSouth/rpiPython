from smbus2 import SMBus
from mlx90614 import MLX90614
import socket
import json
import types

serverAddressPort = ("255.255.255.255", 5005)

# This a fake class, that's just simple to use.
# Attributes are added as soon as you declare them.
x = types.SimpleNamespace()
x.ID = 0


bus = SMBus(1)
sensor = MLX90614(bus, address=0x5A)
x.Temperature = sensor.get_ambient()

# Making some fake data here using the object temperature
x.CO2 = sensor.get_object_1() * 27

# Same with humidity
x.Humidity = sensor.get_object_1() * 2.1
bus.close()

print("Temperature:", x.Temperature)
print("CO2:", x.CO2)
print("Humidity:", x.Humidity)

# It doesn't know how to serialize it, so the default stuff has be included. "It just works (TM)"
json_string = json.dumps(x, default=lambda o: o.__dict__)
bytesToSend = str.encode(json_string)


# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Broadcast is disabled by default. Need to allow manually.
UDPClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPort)