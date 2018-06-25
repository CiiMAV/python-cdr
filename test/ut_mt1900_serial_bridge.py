import serial
import time
import binascii
print( b'2'==b'\x32')
port = serial.Serial('/dev/ttyUSB1',9600,timeout=0.15)
ser = serial.Serial('/dev/ttyUSB0',9600,timeout=0.15)
port.flushInput()
ser.flushInput()
port.flushOutput()
ser.flushOutput()
while True:
	data = b''
	while ser.in_waiting:
		data = data + ser.readline()
		pass
	if len(data) != 0:
		print('send: %s'%data)
		pass
	port.write(data)

	data = b''
	while port.in_waiting:
		data = data + port.readline()
		pass
	if len(data) != 0:
		print('read: %s'%data)
		pass
	ser.write(data)

	pass