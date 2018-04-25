import ctypes

libc = ctypes.CDLL("./libhelloworld.so", mode=ctypes.RTLD_GLOBAL)

x = ctypes.c_char_p("Hello")

libc.foo(1,x,5)