import ctypes
import sys
lib = ctypes.cdll.LoadLibrary('./sensor_accel_cdr.so')

class sensor_accel(object):
	"""docstring for sensor_accel"""
	def __init__(self):
		lib.sensor_accel_new.restype = ctypes.c_void_p
		lib.sensor_accel_deserialize.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int]
		lib.sensor_accel_deserialize.restype = ctypes.c_void_p
		lib.get_m_x.argtype = ctypes.c_void_p
		lib.get_m_x.restype = ctypes.c_float
		self.obj = lib.sensor_accel_new()
		self.m_x = 0
	def get_m_x(self):
		self.m_x = lib.get_m_x(self.obj)
		return self.m_x;
	def deserialize(self,data,length):
		lib.sensor_accel_deserialize(self.obj,data,length )
		self.get_m_x()

