#microRTPS_bridge for raspberry pi

#CONFIG
PYTHON_VERSION = True


#import
import sys
import serial
import numpy as np 
import ctypes
import threading
import time
import logging
import struct
import psutil
from queue import Queue
from PyCRC.CRC16 import CRC16


#import wraper modules
from lib_sensor_baro_cdr import sensor_baro 
from lib_sensor_accel_cdr import sensor_accel 
from lib_raspi_cdr import raspi 

#import VL53L0X library
import VL53L0X
#import startup
import lib_startup

# python version
if PYTHON_VERSION:
	print(sys.version)
	print(psutil.cpu_times())
	pass

# logging
logger    = logging.getLogger('microRTPS_log')
formatter = logging.Formatter('[%(levelname)s] %(asctime)s (%(threadName)-10s) %(message)s')
log_file  = logging.FileHandler('microRTPS_log.log', mode='w')
log_file.setFormatter(formatter)
log_cmd = logging.StreamHandler()
log_cmd.setFormatter(formatter)
logger.addHandler(log_file)
logger.addHandler(log_cmd)
logger.setLevel(logging.DEBUG)


# global variables
ranger_q = Queue()

def serial_read_thread(run_event):
	logger.debug('starting')
	
	############################
	port_name     = '/dev/serial0'
	port_baudrate = 460800
	port          = serial.Serial(port_name,460800)
	############################
	msg_count     = 0
	buf           = ctypes.create_string_buffer(b'',1000)
	loop          = 0
	ST_accel      = sensor_accel()
	############################
	try:
		while run_event.is_set():
			hat_count = 0
			while hat_count != 3:
				if port.read() ==b'>':
					hat_count += 1
					pass
				loop +=1
				if loop % 100 == 0:
					logger.debug('no hat')
					pass
				pass
			found_msg = True
			msg_count += 1
			if found_msg == True:
				port.timeout = 0.01
				x = port.read(6)

				len_h,len_l =  np.frombuffer(x,dtype='uint8',count=2,offset=2)
				len_h = len_h.astype('uint16')
				len_l = len_l.astype('uint16')
				payload_len = np.left_shift(len_h,8) + len_l

				crc_h,crc_l = np.frombuffer(x,dtype='uint8',count=2,offset=4)
				crc_h = crc_h.astype('uint16')
				crc_l = crc_l.astype('uint16')
				read_crc = np.left_shift(crc_h,8) + crc_l

				#logger.info('read_crc: %d'%read_crc)

				#read payload
				data = port.read(payload_len)
				#calculate crc of payload
				cal_crc = CRC16().calculate(data)
				#compare crc
				if read_crc != cal_crc:
					print("BAD CRC")
					continue
					pass
				buf = data
				#logger.info(x[0])
				if x[0] == 56:
					ST_accel.deserialize(buf,1000)
					ST_accel.get_m_x()
					logger.info("%6.4f"%ST_accel.m_x)
					pass

				pass
			pass
		pass
	except Exception as e:
		logger.debug(e)
		pass
	############################

	logger.debug('exiting')
	pass

def serial_write_thread(q,run_event):
	logger.debug('starting')

	############################
	port_name     = '/dev/serial0'
	port_baudrate = 460800
	port          = serial.Serial(port_name,460800)
	############################
	reverse   = False
	msg_count = 0
	topic_ID  = 0
	seq       = 0
	buf       = ctypes.create_string_buffer(b'',1000)
	ST 	      = raspi()
	############################
	try:
		while run_event.is_set():
			
			
			val = 0
			try:
				val = q.get_nowait()
				pass
			except Exception as e:
				continue
				pass

			if val[0] > 800 or val[0] < 0:
				continue
				pass
			if val[1] > 800 or val[1] < 0:
				continue
				pass

			range_dif = val[0]-val[1]
			if reverse == True:
				range_dif = -range_dif
				pass


			ST.set_m_value(range_dif)
			ST.serialize(buf,1000)
			Len = np.array(ST.get_length(), dtype = np.uint16)
			topic_ID = 95

			seq += 1
			if seq == 256:
				seq = 0
				pass
	
			payload_len_l = np.frombuffer(Len,dtype='uint8',count=1,offset=0)
			payload_len_h = np.frombuffer(Len,dtype='uint8',count=1,offset=1)
			payload_len = np.left_shift(payload_len_h,8) + payload_len_l
	
			serialized = buf[0:payload_len[0]]
	
			cal_crc = CRC16().calculate(serialized)
			
			cal_crc = np.array(cal_crc, dtype = np.uint16)
			crc_l = np.frombuffer(cal_crc,dtype='uint8',count=1,offset=0)
			crc_h = np.frombuffer(cal_crc,dtype='uint8',count=1,offset=1)
	
			#pack header
			data = [b'>',b'>',b'>',topic_ID,seq,payload_len_h[0],payload_len_l[0],crc_h[0],crc_l[0]]
	
			st_data = struct.pack('<3c6B',*data)
			st_data += serialized
	
			k = port.write(st_data)
			logger.info("send: %d"%k)
			time.sleep(0.01)
			pass
		pass
	except Exception as e:
		raise e
	############################

	logger.debug('exiting')
	pass

def ranger_read_thread(q,run_event):
	logger.debug('starting')

	# Create a VL53L0X object for device on TCA9548A bus 1
	tof1 = VL53L0X.VL53L0X(TCA9548A_Num=1, TCA9548A_Addr=0x70)
	# Create a VL53L0X object for device on TCA9548A bus 2
	tof2 = VL53L0X.VL53L0X(TCA9548A_Num=2, TCA9548A_Addr=0x70)

	# Start ranging on TCA9548A bus 1
	tof1.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
	# Start ranging on TCA9548A bus 2
	tof2.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

	timing = tof1.get_timing()
	if (timing < 20000):
		timing = 20000
	logger.debug("Timing %d ms" % (timing/1000))
	try:	
		for count in range(1,10000):
			if not run_event.is_set():
				return
				pass
			# Get distance from VL53L0X  on TCA9548A bus 1
			distance1 = tof1.get_distance()
			# Get distance from VL53L0X  on TCA9548A bus 2
			distance2 = tof2.get_distance()
			if distance1>0 and distance2>0:
				logger.info("1: %6d mm    2: %6d mm    cnt: %6d"% (distance1,distance2,count))
				#pack
				ranger_dist = [distance1,distance2]
				q.put(ranger_dist)
				pass
			pass
		pass
	except Exception as e:
		logger.debug('error in for loop: '+ repr(e))
		pass
	logger.debug('exiting')
	pass

def main():	
	lib_startup.start()
	run_event = threading.Event()
	run_event.set()
	#thread init
	read_thread   = threading.Thread(name='serial_read_thread ', target= serial_read_thread , args=(run_event,))
	write_thread  = threading.Thread(name='serial_write_thread', target= serial_write_thread, args=(ranger_q,run_event,))
	ranger_thread = threading.Thread(name='ranger_read_thread' , target= ranger_read_thread , args=(ranger_q,run_event,))
	#start
	read_thread.start()
	write_thread.start()
	ranger_thread.start()
	try:
		while True:
			logger.info("cpu_percent: %4d, mem_percent: %4d"%(psutil.cpu_percent(interval=1), psutil.virtual_memory().percent))
			time.sleep(0.1)
		pass
	except KeyboardInterrupt:
		logging.info("KeyboardInterrupt, close all threads")
		run_event.clear()
		
		read_thread.join()
		write_thread.join()
		ranger_thread.join()

		logger.info("threads successfully closed")
	pass

if __name__ == '__main__':
	main()