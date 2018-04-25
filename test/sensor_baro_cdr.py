import ctypes
import sys
lib = ctypes.cdll.LoadLibrary('./cdr.so')

class sensor_baro(object):
	"""docstring for sensor_baro"""
	def __init__(self):
		#lib.sensor_baro_new.argtypes = [ctypes.c_void_p]
		lib.sensor_baro_new.restype = ctypes.c_void_p
		lib.sensor_baro_deserialize.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int]
		lib.sensor_baro_deserialize.restype = ctypes.c_void_p
		lib.get_altitude.argtype = ctypes.c_void_p
		lib.get_altitude.restype = ctypes.c_float
		self.obj = lib.sensor_baro_new()
		self.altitude = 0.0
	def get_altitude(self):
		self.altitude = lib.get_altitude(self.obj)
		return self.altitude
	def deserialize(self,data,length):
		lib.sensor_baro_deserialize(self.obj,data,length )
		self.get_altitude()
	
		
ST = sensor_baro()

print(ST)

buf = ctypes.create_string_buffer(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 A\x00\x00\x00\x00\x00\x00\x00\x00',1000)
print(ctypes.sizeof(buf))

print("test")
print(buf.raw)
ST.deserialize(buf,1000)
print(buf.raw)


ST.get_altitude()
print(ST.altitude)

#b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 A\x00\x00\x00\x00\x00\x00\x00\x00'
#b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc8B\x00\x00\x00\x00\x00\x00\x00\x00'

buf = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc8B\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc8B\x00'
print(buf[1])
print(buf[2])

ST.deserialize(buf,1000)

x = ST.get_altitude()
print(ST.altitude)
print(x)