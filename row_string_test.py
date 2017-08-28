import os
import serial
from serial_read import read_arduino_serial, take_last_observation

p = os.environ.get("PORT_NAME")
#arduino = serial.Serial(p, 9600, timeout = 20)
#print(take_last_observation(arduino))
print(read_arduino_serial(p, 9600))