import serial
import numpy as np 
import ctypes
from PyCRC.CRC16 import CRC16
import struct
import time

from lib_sensor_accel_cdr import sensor_accel
from lib_sensor_baro_cdr import sensor_baro
from lib_raspi_cdr import raspi
print(np.version.version)
ser = serial.Serial('/dev/serial0',460800)

ST = raspi()
ST2 = raspi()

print("start loop")
msg_cnt = 0
seq = 0
buf = ctypes.create_string_buffer(b'',1000)
k = bytearray([1, 2, 3])
print(k)
vhex = np.vectorize(np.binary_repr)
while True:
	ST.set_m_value(seq)
	ST.serialize(buf,1000)
	#print(buf)
	#print(buf.raw)
	Len = np.array(ST.get_length(), dtype = np.uint16)
	#print(Len)
	#prepare header
	print(seq)
	topic_ID = 95
	seq += 1
	if seq == 256:
		seq = 0
		pass

	payload_len_l = np.frombuffer(Len,dtype='uint8',count=1,offset=0)
	payload_len_h = np.frombuffer(Len,dtype='uint8',count=1,offset=1)
	payload_len = np.left_shift(payload_len_h,8) + payload_len_l

	#print(payload_len)
	serialized = buf[0:payload_len[0]]
	#for i in range(payload_len[0]+1):
		#print(buf[i])
	#	pass
	#print(serialized)
	cal_crc = CRC16().calculate(serialized)
	#print(cal_crc)

	cal_crc = np.array(cal_crc, dtype = np.uint16)
	crc_l = np.frombuffer(cal_crc,dtype='uint8',count=1,offset=0)
	crc_h = np.frombuffer(cal_crc,dtype='uint8',count=1,offset=1)

	ST2.deserialize(buf,1000)
	#print(ST2.get_m_value())
	ST2.deserialize(b'\xcd\xcc\xf6B',1000)
	#print(ST2.get_m_value())
	#pack header
	data = [b'>',b'>',b'>',topic_ID,seq,payload_len_h[0],payload_len_l[0],crc_h[0],crc_l[0]]
	#print(data)
	st_data = struct.pack('<3c6B',*data)
	#print(st_data)
	#print(struct.calcsize('3c6B'))

	st_data += serialized
	#print(st_data)

	ser.write(st_data)
	time.sleep(0.01)
	pass