import customtkinter as ctk
from translate import translate
from clipboard import paste_traslation
import asyncio
class Popup:
    def __init__(self, root=None):
        self.root = root or ctk.CTk()
        self.root.withdraw()
        self.base_text = ""
        self.translated_text = ""
        self.last_window = int | None
        


        self.window = ctk.CTkToplevel(self.root)
        #self.window.wm_attributes("-alpha",0.8)
        self.window.attributes("-topmost", True)
        self.window.overrideredirect(True)

        self.frame = ctk.CTkFrame(self.window, corner_radius=0)
        self.frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.entry = ctk.CTkEntry(self.frame, width=570, corner_radius=0)
        self.entry.pack(pady=(5,5))



        self.window.bind("<Return>", self.traslate_text)
        self.window.bind("<Escape>", self.close)
        self.window.bind("<FocusOut>", self.close)
        self.window.withdraw()


    def center_popup(self, height=60, width=600):
        screen_height = self.window.winfo_screenheight()
        screen_width = self.window.winfo_screenwidth ()
        
        x = (screen_height - height) // 2
        y = (screen_width - width) // 2

        self.window.geometry(f"{width}x{height}+{(x+200)}+{(y)}")

        


    #Regresa el contenido actual de la variable de la traduccion
    def get_base_text(self):
        return self.base_text
    
    #Otorga valor a la variable que almacena la traducion
    def set_base_text(self, text):
        self.base_text = text

    def set_translated_text(self, translated :str):
        self.translated_text = translated
    
    def get_translated_text(self):
        return self.translated_text
    
    def get_last_window(self):
        return self.last_window
    def set_last_window(self, hwnd_window):
        self.last_window = hwnd_window

    

    #Muestra la ventana, limpia el entry y obtiene el foco
    def show(self):
        self.center_popup()
        self.window.deiconify()
        self.entry.delete(0, "end")
        self.entry.focus_force()


    #Esconde la ventana
    def close(self, event=None):
        self.window.withdraw()

    #traducira el texto y guarda valores en las variables
    def traslate_text(self, event=None):
        self.set_base_text(str(self.entry.get()))
        self.set_translated_text(asyncio.run(translate(text_=self.get_base_text(), from_="es", to_="en")))
        if self.get_translated_text() is not None:

            paste_traslation(text=self.get_translated_text(), hwnd_window=self.get_last_window())
            self.close()

    def focus_out():
        pass

    

    

test : bool = False
if test:
    mypop = Popup()
    mypop.show()
    mypop.center_popup()
    mypop.root.mainloop()