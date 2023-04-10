from tkinter import *
from .custom_frame import CustomFrame,small_text_size,large_text_size

class Weather(Frame):
    temperature = ''
    forecast = ''
    icon = ''

    def __init__(self, parent, **kwargs):
        CustomFrame.__init__(self, parent, kwargs)
        #Create Degree frame
        self.degreeFrm = Frame(self, bg=self.background)
        self.degreeFrm.pack(side=TOP, anchor=W)
        #Create Temperature frame
        self.temperatureLbl = Label(self.degreeFrm, font=(self.fontStyle, large_text_size), fg=self.fontColor, bg=self.background)
        self.temperatureLbl.pack(side=LEFT, anchor=N)
        #Create Icon frame
        self.iconLbl = Label(self.degreeFrm, bg=self.background)
        self.iconLbl.pack(side=LEFT, anchor=S, padx=20)
        #Create Forecast frame
        self.forecastLbl = Label(self, font=(self.fontStyle, small_text_size), fg=self.fontColor, bg=self.background)
        self.forecastLbl.pack(side=RIGHT, anchor=W, padx=20)

    def set_icon(self,icon_image):
        self.iconLbl.config(image=icon_image)
        self.iconLbl.image = icon_image

    def set_forecast(self,new_forecast):
        if self.forecast != new_forecast:
            self.forecast = new_forecast
            self.forecastLbl.config(text=new_forecast)

    def set_temperature(self,new_temperature):
        if self.temperature != new_temperature:
            self.temperature = new_temperature
            self.temperatureLbl.config(text=new_temperature)