import serial
import numpy as np 
import ctypes
from PyCRC.CRC16 import CRC16

from lib_sensor_baro_cdr import sensor_baro
from lib_sensor_accel_cdr import sensor_accel

print(np.version.version)

ser = serial.Serial('/dev/serial0',460800)

ST_baro = sensor_baro()
ST_accel = sensor_accel()

buf = ctypes.create_string_buffer(b'\x00',1000)

print("go to loop")
msg_cnt = 0
while True:
	#print(":")
	hat_count = 0
	while(hat_count != 3):
		x = ser.read()
		#print(x)
		if x == b'>':
			hat_count +=1 
			#print("found header")
		pass

	msg_cnt += 1
	found_msg = True
	print("found msg : %s"%msg_cnt)

	if found_msg == True:
		ser.timeout = 0.01
		x = ser.read(6)
		print(x)		
		#print(x)
		#print(type(x))
		#read payload length
		len_h,len_l =  np.frombuffer(x,dtype='uint8',count=2,offset=2)
		len_h = len_h.astype('uint16')
		len_l = len_l.astype('uint16')
		payload_len = np.left_shift(len_h,8) + len_l
		#print(payload_len)

		#read crc
		crc_h,crc_l = np.frombuffer(x,dtype='uint8',count=2,offset=4)
		crc_h = crc_h.astype('uint16')
		crc_l = crc_l.astype('uint16')
		read_crc = np.left_shift(crc_h,8) + crc_l
		#print(read_crc)

		#read payload
		data = ser.read(payload_len)
		#print(data)

		#calculate crc of payload
		cal_crc = CRC16().calculate(data)

		#compare crc
		if read_crc != cal_crc:
			print("BAD CRC")
			continue
			pass
		pass

		#print("VALID CRC")

		#print(data)
		#print(type(data))
		buf = data
		print(x[0])
		if x[0] == 57:
			ST_baro.deserialize(buf,1000)
			ST_baro.get_altitude()
			print(ST_baro.altitude)
			pass
		elif x[0] == 56:
			ST_accel.deserialize(buf,1000)
			ST_accel.get_m_x()
			print("%.4f"%ST_accel.m_x)
			pass
		
	pass