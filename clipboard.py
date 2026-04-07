import pyperclip
import win32gui
import win32con
import win32api
import time
from pynput.keyboard import Controller, Key

keyboard = Controller()

def paste_traslation(text, hwnd_window):
    try:
        last_clipboard = pyperclip.paste()
    except:
        last_clipboard = ''
    pyperclip.copy(text)
    time.sleep(0.05)

    try:
        win32gui.ShowWindow(hwnd_window, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd_window)
    except Exception as e:
        print("unable to restore windows focus", e)

        return
    time.sleep(0.3)
    win32api.keybd_event(win32con.VK_CONTROL,0,0,0)
    win32api.keybd_event(ord('V'),0,0,0)
    win32api.keybd_event(ord('V'),0,win32con.KEYEVENTF_KEYUP,0)
    win32api.keybd_event(win32con.VK_CONTROL,0,win32con.KEYEVENTF_KEYUP,0)
    



    """
    with keyboard.pressed(Key.ctrl):
        keyboard.press('V')
        time.sleep(1)
        keyboard.release('V')
    time.sleep(0.1)
    """

    pyperclip.copy(last_clipboard)
