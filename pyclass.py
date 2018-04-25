import ctypes

lib = ctypes.cdll.LoadLibrary('./libclass.so')

class Foo(object):
    def __init__(self, val):
        lib.Foo_new.argtypes = [ctypes.c_int]
        lib.Foo_new.restype = ctypes.c_void_p
        lib.Foo_bar.argtypes = [ctypes.c_void_p]
        lib.Foo_bar.restype = ctypes.c_void_p
        lib.Foo_foobar.argtypes = [ctypes.c_void_p, ctypes.c_int]
        lib.Foo_foobar.restype = ctypes.c_int
        self.obj = lib.Foo_new(val)
    def bar(self):
        lib.Foo_bar(self.obj)
    
    def foobar(self, val):
        return lib.Foo_foobar(self.obj, val)

f = Foo(5)

f.bar()

print f.foobar(7)

x = f.foobar(2)

print type(x)