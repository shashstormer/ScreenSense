import psutil
import win32gui
import win32process
from config import inactivity_threshold_seconds
import ctypes
from PIL import ImageGrab
import time
from io import BytesIO
from .do_input_event import send_fake_input
import numpy as np


class LastInputInfo(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_ulong)]


def get_last_input_time():
    lii = LastInputInfo()
    lii.cbSize = ctypes.sizeof(LastInputInfo)
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
    millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
    return millis / 1000.0


def check_inactivity_threshold(threshold_seconds=inactivity_threshold_seconds):
    last_input_time = get_last_input_time()
    if last_input_time > threshold_seconds:
        return True
    else:
        return False


def take_screenshot():
    with ImageGrab.grab() as screenshot:
        return screenshot


def compare_screenshots(screenshot1, screenshot2):
    # Convert screenshots to numpy arrays for comparison
    img_array1 = np.array(screenshot1)
    img_array2 = np.array(screenshot2)

    # Calculate the mean absolute difference between the two images
    diff = np.sum(np.abs(img_array1 - img_array2)) / float(img_array1.size)

    return diff


def get_window_title_by_pid(pid):
    try:
        process = psutil.Process(pid)
        window_title = None

        def callback(hwnd, _):
            nonlocal window_title
            _, process_id = win32process.GetWindowThreadProcessId(hwnd)
            if process_id == pid:
                window_title = win32gui.GetWindowText(hwnd)

        win32gui.EnumWindows(callback, None)
        return window_title
    except Exception as e:
        print(e)
        return None


def is_user_active():
    active = not check_inactivity_threshold()
    try:
        if not active:
            screenshot1 = take_screenshot()
            time.sleep(1)
            screenshot2 = take_screenshot()
            diff = compare_screenshots(screenshot1, screenshot2)
            if diff > 0.1:
                print("User may be active")
                active = True
                send_fake_input()
    except Exception as e:
        print(e)
    return active


def processes_exes():
    for process in psutil.process_iter(['pid', 'name', 'exe', 'cmdline', 'cwd', 'create_time', 'status',
                                        'username', 'cpu_percent', 'memory_percent', 'connections',
                                        'open_files', 'threads', 'environ']):
        yield (process.pid, process.name(), process.exe(), process.cmdline(), process.cwd(),
               process.create_time(), process.status(), process.username(),
               process.cpu_percent(), process.memory_percent(), process.connections(),
               process.open_files(), process.threads(), process.environ())


def active_window_details(iter_count=0):
    if iter_count > 300:
        return False, False, False, False, False, False
    foreground_window = win32gui.GetForegroundWindow()
    _, process_id = win32process.GetWindowThreadProcessId(foreground_window)
    try:
        process = psutil.Process(process_id)
    except (psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess, ValueError):
        try:
            return active_window_details(iter_count + 1)
        except RecursionError:
            return False, False, False, False, False, False
    except Exception as e:
        print(e)
        return False, False, False, False, False, False
    process_name = process.name()
    process_exe = process.exe()
    command = process.cmdline()
    window_title = win32gui.GetWindowText(foreground_window)
    return process_name, process_id, process_exe, window_title, command, True
