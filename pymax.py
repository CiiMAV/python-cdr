from ctypes import *
cmax = cdll.LoadLibrary('./test.dll').max
cmax.argtypes = [c_int, c_int]
cmax.restype = c_int
x = cmax(4,7)
print x