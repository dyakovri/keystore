from ctypes import c_char_p
from multiprocessing import Value


token = Value(c_char_p, b"/")
