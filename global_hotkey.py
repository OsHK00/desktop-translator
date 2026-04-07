from pynput import keyboard
import threading
from popup import Popup
import win32gui
instance = Popup()

def on_activate():
    last_window = win32gui.GetForegroundWindow()
    instance.set_last_window(hwnd_window=last_window)
    threading.Thread(target=instance.show).start()    
    
def stop_prosess():
    print("closing hotkeys. . .")
    hotkey.stop() 
    instance.root.destroy()

#pruebas-----------------
def show_traslation():
    print("Contenido de la readucion: ",instance.get_translated_text())
    pass


hotkey = keyboard.GlobalHotKeys({
    '<ctrl>+<shift>+0' : on_activate,
    '<ctrl>+<shift>+9' : stop_prosess,
    '<ctrl>+<shift>+8' : show_traslation
})


print("Listenig Hotkeys. . .")

hotkey.start()
instance.root.mainloop()
hotkey.join()

print("Program closed")



