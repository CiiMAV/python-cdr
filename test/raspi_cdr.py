import ctypes
import sys
lib = ctypes.cdll.LoadLibrary('./raspi_cdr.so')

class raspi(object):
	"""docstring for raspi"""
	def __init__(self):
		lib.raspi_new.restype = ctypes.c_void_p
		
		lib.raspi_deserialize.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int]
		lib.raspi_deserialize.restype = ctypes.c_void_p
		lib.raspi_serialize.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int]
		lib.raspi_serialize.restype = ctypes.c_void_p
		
		lib.get_m_value.restype = ctypes.c_float
		lib.get_length.restype = ctypes.c_int

		lib.set_m_value.argtypes = [ctypes.c_void_p,ctypes.c_float]
		self.obj = lib.raspi_new()
		self.m_value = 0.0
		self.length  = 0
	def get_m_value(self):
		self.m_value = lib.get_m_value(self.obj)
		return self.m_value
	def get_length(self):
		self.length = lib.get_length(self.obj)
		return self.length
	def deserialize(self,data,length):
		lib.raspi_deserialize(self.obj,data,length)
		self.get_m_value()
	def serialize(self,data,length):
		lib.raspi_serialize(self.obj,data,length)
		self.get_length()
	def set_m_value(self,val):
		self.m_value = val
		lib.set_m_value(self.obj,self.m_value)
		
ST1 = raspi()
ST2 = raspi()
print(ST1)
print(ST2)

buf1 = ctypes.create_string_buffer(b'',1000)
buf2 = ctypes.create_string_buffer(b'',1000)

ST1.m_value = 100.0
print(ST1.m_value)
ST1.set_m_value(123.1)
print(ST1.get_m_value())
print(buf1.raw)
ST1.serialize(buf1,1000)
print(buf1.raw)
print(ST1.length)
ST2.deserialize(buf1,1000)
print(ST2.m_value)
