from multiprocessing import Value
from ctypes import c_char_p


token = Value(c_char_p, b"/")
