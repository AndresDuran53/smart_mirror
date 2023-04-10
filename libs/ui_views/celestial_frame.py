from tkinter import *
from .custom_frame import CustomFrame,small_text_size

class MoonFrame(Frame):
    icon = ''

    def __init__(self, parent, **kwargs):
        CustomFrame.__init__(self, parent, kwargs)
        #Create Phase frame
        self.nextMoonFrm = Frame(self, bg=self.background)
        self.nextMoonFrm.pack(side=LEFT, anchor=W)
        #Create nextFullMoon frame
        self.nextFullMoonLbl = Label(self.nextMoonFrm, text="", font=(self.fontStyle, small_text_size), fg=self.fontColor, bg=self.background)
        self.nextFullMoonLbl.pack(side=TOP, anchor=N)
        #Create nextFullMoon frame
        self.dateNextFullMoonLbl = Label(self.nextMoonFrm, text="", font=(self.fontStyle, small_text_size), fg="#AAAAAA", bg=self.background)
        self.dateNextFullMoonLbl.pack(side=BOTTOM, anchor=E)

        #Create Phase frame
        self.phaseFrm = Frame(self, bg=self.background)
        self.phaseFrm.pack(side=RIGHT, anchor=E)
        #Create Icon frame
        self.iconLbl = Label(self.phaseFrm, bg=self.background)
        self.iconLbl.pack(side=TOP, anchor=N, padx=20)
        #Create Forecast frame
        self.illuminationLbl = Label(self.phaseFrm, text="", font=(self.fontStyle, small_text_size), fg=self.fontColor, bg=self.background)
        self.illuminationLbl.pack(side=BOTTOM, anchor=S, padx=20)

    def set_icon(self,icon_image):
        self.iconLbl.config(image=icon_image)
        self.iconLbl.image = icon_image

    def set_illumination(self,illumination):
        self.illuminationLbl.config(text=illumination)

    def set_nextFullMoonLbl(self,date):
        self.nextFullMoonLbl.config(text="Next full moon")
        self.dateNextFullMoonLbl.config(text=date)

class SunsetFrame(Frame):
    icon = ''

    def __init__(self, parent, **kwargs):
        CustomFrame.__init__(self, parent, kwargs)
        #Create Phase frame
        self.nextSunsetFrm = Frame(self, bg=self.background)
        self.nextSunsetFrm.pack(side=LEFT, anchor=W)
        #Create next Sunset frame
        self.nextFullSunsetLbl = Label(self.nextSunsetFrm, text="", font=(self.fontStyle, small_text_size), fg=self.fontColor, bg=self.background)
        self.nextFullSunsetLbl.pack(side=TOP, anchor=N)
        
        self.dateNextFullSunsetLbl = Label(self.nextSunsetFrm, text="", font=(self.fontStyle, small_text_size), fg="#AAAAAA", bg=self.background)
        self.dateNextFullSunsetLbl.pack(side=BOTTOM, anchor=E)

        #Create Icon frame
        self.iconLbl = Label(self, bg=self.background)
        self.iconLbl.pack(side=RIGHT, anchor=E, padx=20)
        

    def set_icon(self,icon_image):
        self.iconLbl.config(image=icon_image)
        self.iconLbl.image = icon_image

    def set_nextSunsetLbl(self,text,date):
        self.nextFullSunsetLbl.config(text=f"Next {text}")
        self.dateNextFullSunsetLbl.config(text=date)