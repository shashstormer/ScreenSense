import ctypes

INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2


class INPUT(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("union", ctypes.POINTER(ctypes.c_ulong))]


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]


def send_fake_input():
    mouse_input = MOUSEINPUT(1, 1, 0, 0x0001, 0, None)
    input_struct = INPUT(INPUT_MOUSE, ctypes.pointer(mouse_input))
    ctypes.windll.user32.SendInput(1, ctypes.pointer(input_struct), ctypes.sizeof(INPUT))
