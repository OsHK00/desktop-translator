import pyperclip
import win32gui
import win32con
import win32api
import time
from pynput.keyboard import Controller, Key

import logging

keyboard = Controller()

logger = logging.getLogger(__name__)
def paste_traslation(text, hwnd_window, win_mode):
    try:
        last_clipboard = pyperclip.paste()
    except:
        last_clipboard = ''
    pyperclip.copy(text) 
    time.sleep(0.2)

    try:
        if win_mode == 1:
            win32gui.ShowWindow(hwnd_window, win32con.SW_NORMAL) 
        if win_mode == 3:
            win32gui.ShowWindow(hwnd_window, win32con.SW_MAXIMIZE)
        win32gui.SetForegroundWindow(hwnd_window)
    except Exception as e:
        logger.error("unable to restore windows focus: %s", e)

        return
    time.sleep(0.2)
    win32api.keybd_event(win32con.VK_CONTROL,0,0,0)
    win32api.keybd_event(ord('V'),0,0,0)
    time.sleep(0.1)
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
