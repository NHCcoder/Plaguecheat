import ctypes
import threading
from time import time

# Constant for mouse input
MOUSEEVENTF_MOVE = 0x0001


# ctypes structures for mouse input
class MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]


class INPUT(ctypes.Structure):
    class _INPUT_UNION(ctypes.Union):
        _fields_ = [("mi", MOUSEINPUT)]

    _anonymous_ = ("u",)
    _fields_ = [("type", ctypes.c_ulong),
                ("u", _INPUT_UNION)]


# ctypes function prototypes
SendInput = ctypes.windll.user32.SendInput
SendInput.argtypes = (ctypes.c_uint, ctypes.POINTER(INPUT), ctypes.c_int)
SendInput.restype = ctypes.c_uint

GetCursorPos = ctypes.windll.user32.GetCursorPos
GetCursorPos.argtypes = [ctypes.POINTER(ctypes.c_long * 2)]
GetCursorPos.restype = ctypes.c_bool

# Global state
last_moved = threading.Lock()
last_moved_time = time()


# Helper function to create mouse input
def create_mouse_input(flags, dx, dy, data, extra_info):
    mi = MOUSEINPUT(dx=dx, dy=dy, mouseData=data, dwFlags=flags, time=0, dwExtraInfo=ctypes.pointer(ctypes.c_ulong(extra_info)))
    input = INPUT(type=0, u=INPUT._INPUT_UNION(mi=mi))
    return input


# Function to send input
def send_input(input):
    SendInput(1, ctypes.byref(input), ctypes.sizeof(input))


# Function to move mouse
def move_mouse(x, y, set_last_moved):
    send_input(create_mouse_input(MOUSEEVENTF_MOVE, x, y, 0, 0))
    if set_last_moved:
        global last_moved_time
        with last_moved:
            last_moved_time = time()
