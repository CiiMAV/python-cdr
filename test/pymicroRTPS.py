#microRTPS_bridge for raspberry pi

#CONFIG
PYTHON_VERSION = True
SERIAL_READ_THREAD = False
SERIAL_WRITE_THREAD = True
RANGER_READ_THREAD = True
BIAS = -6

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
import PyCRC
import coloredlogs
from PyCRC.CRC16 import CRC16



#import wraper modules
from lib_sensor_baro_cdr import sensor_baro 
from lib_sensor_accel_cdr import sensor_accel 
from lib_raspi_cdr import raspi 

#import VL53L0X library
import VL53L0X

#import MPU6050
from MPU6050 import MPU6050

#import startup
import lib_startup

# python version
if PYTHON_VERSION:
	print(sys.version)
	print(sys.path)
	print(PyCRC.__file__)
	print(psutil.cpu_times())
	pass

# logging

timestr = time.strftime("%Y%m%d-%H%M%S")
logger    = logging.getLogger('microRTPS_log')
formatter = logging.Formatter('[%(levelname)s] %(asctime)s (%(threadName)-10s) %(message)s')
log_file  = logging.FileHandler('microRTPS_log_'+timestr+'.log', mode='w')
log_file.setFormatter(formatter)
log_cmd = logging.StreamHandler()
log_cmd.setFormatter(formatter)
logger.addHandler(log_file)
logger.addHandler(log_cmd)
logger.setLevel(logging.INFO)

coloredlogs.install(logger=logger,milliseconds=True,fmt='%(asctime)s,%(msecs)03d %(threadName)40s %(levelname)10s %(message)s')

# global variables
ranger_q = Queue()

def serial_read_thread(run_event):
	logger.critical('starting')
	
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
		last_time = time.process_time()
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
			logger.debug("msg read: %6d"%msg_count)
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
					logger.warning("BAD CRC")
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

			#current_time =  time.process_time()
			#logger.critical("loop time : %6.4f"%(current_time-last_time))
			#last_time = current_time
			pass
		pass
	except Exception as e:
		logger.critical(e)
		pass
	############################

	logger.critical('exiting')
	pass

def serial_write_thread(q,run_event):
	logger.critical('starting')

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
		last_time = time.process_time()
		while run_event.is_set():
			
			cnt = 0

			val = 0
			try:
				val = q.get(timeout=0.4)
				cnt = 1
				if val[0] > 800  or val[1] > 800  :
					cnt = 0
					pass
				pass
			except Exception as e:
				val = [0,0]
				pass

			cnt1 = 0

			val1 = 0
			try:
				val1 = q.get(timeout=0.4)
				cnt1 = 1
				if val1[0] > 800  or val1[1] > 800  :
					cnt1 = 0
					pass
				pass
			except Exception as e:
				val1 = [0,0]
				pass

			cnt2 = 0

			val2 = 0
			try:
				val2 = q.get(timeout=0.4)
				cnt2 = 1
				if val2[0] > 800  or val2[1] > 800  :
					cnt2 = 0
					pass
				pass
			except Exception as e:
				val2 = [0,0]
				pass

			range_dif = cnt*(val[0]-val[1] + BIAS) + cnt1*(val1[0]-val1[1] + BIAS) + cnt2*(val2[0]-val2[1] + BIAS)
			if (cnt+cnt1+cnt2) == 0 :
				continue
				pass
			range_dif = range_dif/(cnt+cnt1+cnt2)
			range_dif = range_dif 
			if reverse == True:
				range_dif = -range_dif
				pass

			#limit 
			if range_dif > 300.0:
				range_dif = 300.0
				pass
			elif range_dif < -300.0:
				range_dif = -300.0
				pass

			#dead zone
			if abs(range_dif) < 16.0:
				range_dif = 0.0
				pass
			elif range_dif > 16.0:
				range_dif = range_dif - 16.0
				pass
			elif range_dif < -16.0:
				range_dif = range_dif + 16.0
				pass

			range_dif  = range_dif * 120.0 / 670.0
			#logger.critical("range_dif: %6d"%range_dif)
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
			msg_count +=1
			logger.info("msg write: %6d"%msg_count)
			logger.debug("send: %d"%k)

			#current_time =  time.process_time()
			#logger.critical("loop time : %6.4f"%(current_time-last_time))
			#last_time = current_time
			time.sleep(0.01)
			pass
		pass
	except Exception as e:
		logger.critical("error in while loop")
		raise e
	############################

	logger.critical('exiting')
	pass

def ranger_read_thread(q,run_event):
	logger.critical('starting')

	#mpu = MPU6050(0x68)

	# Create a VL53L0X object for device on TCA9548A bus 1
	tof1 = VL53L0X.VL53L0X(TCA9548A_Num=1, TCA9548A_Addr=0x70)
	# Create a VL53L0X object for device on TCA9548A bus 2
	tof2 = VL53L0X.VL53L0X(TCA9548A_Num=2, TCA9548A_Addr=0x70)

	# Start ranging on TCA9548A bus 1
	tof1.start_ranging(VL53L0X.VL53L0X_BEST_ACCURACY_MODE)
	# Start ranging on TCA9548A bus 2
	tof2.start_ranging(VL53L0X.VL53L0X_BEST_ACCURACY_MODE)

	timing = tof1.get_timing()
	if (timing < 20000):
		timing = 20000
	logger.info("Timing %d ms" % (timing/1000))

	count = 0
	try:	
		#for count in range(1,10000):
		last_time = time.process_time()
		while True:
			if not run_event.is_set():
				return
				pass

			# Get distance from VL53L0X  on TCA9548A bus 1
			distance1 = tof1.get_distance()
			# Get distance from VL53L0X  on TCA9548A bus 2
			distance2 = tof2.get_distance()
			if distance1>0 and distance2>0:
				count += 1
				logger.info("1: %6d mm    2: %6d mm    cnt: %6d"% (distance1,distance2,count))
				#pack
				ranger_dist = [distance1,distance2]
				q.put(ranger_dist)
				logger.debug("ranger read: %6d"%count)
				pass

				
			#accel_data = mpu.get_accel_data()
			#logger.critical("Accelerometer data")
			#logger.critical("x: " + str(accel_data['x']))
			#logger.critical("y: " + str(accel_data['y']))
			#logger.critical("z: " + str(accel_data['z']))
			#current_time =  time.process_time()
			#logger.critical("loop time : %6.4f"%(current_time-last_time))
			#last_time = current_time
			if time.process_time()-last_time > 30.0*60.0:
				break
				pass
			time.sleep(timing/1000000.00)
			pass
		pass
	except Exception as e:
		logger.critical('error in for loop: '+ repr(e))
		pass
	logger.critical('exiting')
	pass

def main():	
	lib_startup.start()
	run_event = threading.Event()
	run_event.set()
	#thread init
	read_thread   = threading.Thread(name='serial_read_thread                                     ' , target= serial_read_thread , args=(run_event,))
	write_thread  = threading.Thread(name='                  serial_write_thread                  ' , target= serial_write_thread, args=(ranger_q,run_event,))
	ranger_thread = threading.Thread(name='                                     ranger_read_thread' , target= ranger_read_thread , args=(ranger_q,run_event,))
	#start
	if SERIAL_READ_THREAD:
		read_thread.start()
		pass
	if SERIAL_WRITE_THREAD:
		write_thread.start()
		pass
	if RANGER_READ_THREAD:
		ranger_thread.start()
		pass
	
	try:
		while True:
			logger.info("cpu_percent: %4d, cpu_count: %2d, mem_percent: %4d, "%(psutil.cpu_percent(interval=None), psutil.cpu_count(), psutil.virtual_memory().percent))
			logger.critical("cpu_percent_per_core: %s"%str(psutil.cpu_percent(interval=None,percpu=True))[1:-1])
			time.sleep(2)			
		pass
	except KeyboardInterrupt:
		logging.critical("KeyboardInterrupt, close all threads")
		run_event.clear()
		
		read_thread.join()
		write_thread.join()
		ranger_thread.join()

		logger.info("threads successfully closed")
	pass

if __name__ == '__main__':
	main()