from tkinter import *
from .custom_frame import CustomFrame,small_text_size

class WifiCodeFrame(Frame):
    icon = ''

    def __init__(self, parent, wifi_code_icon, **kwargs):
        CustomFrame.__init__(self, parent, kwargs)
        #Create Phase frame
        self.nextMoonFrm = Frame(self, bg=self.background)
        self.nextMoonFrm.pack(side=LEFT, anchor=W)
        #Create Icon frame
        self.iconLbl = Label(self.nextMoonFrm, bg=self.background)
        self.iconLbl.pack(side=TOP, anchor=N, padx=20)
        self.set_icon(wifi_code_icon)

    def set_icon(self,icon_image):
        self.iconLbl.config(image=icon_image)
        self.iconLbl.image = icon_image