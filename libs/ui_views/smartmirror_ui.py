from tkinter import *
from .picture_frame import PictureFrame
from .celestial_frame import MoonFrame,SunsetFrame
from .wifi_code_frame import WifiCodeFrame
from .calendar_frame import Calendar
from .clock_frame import Clock
from .weather_frame import Weather
from .countdown.general_countdown_frame import GeneralCountdown
from .videocamera_frame import VideoFrame

class FullscreenWindow:
    padding_x = 30
    padding_y = 60
    fontColor = "white"
    background = "black"
    fontStyle = "Roboto Medium"

    def __init__(self):
        self.tk = Tk()
        self.tk.configure(background=self.background)
        self.w = self.tk.winfo_screenwidth()
        self.h = self.tk.winfo_screenheight()
        self.topFrame = Frame(self.tk, background = self.background)
        self.midFrame = Frame(self.tk, background = self.background)
        self.topFrame.pack(side = TOP, fill=X)
        self.midFrame.pack(side = TOP, fill=BOTH, expand = YES)
        self.tk.attributes("-fullscreen", True)

    def create_weather_frame(self):
        self.weather = Weather(self.topFrame, 
                                background_parent = self.background, 
                                fontColor_parent = self.fontColor, 
                                fontStyle_parent = self.fontStyle)
        self.weather.pack(side=RIGHT, padx=self.padding_x, pady=self.padding_y)
        self.weather.pack_forget()

    def create_moon_frame(self):
        self.moon_frame = MoonFrame(self.midFrame, 
                                background_parent = self.background, 
                                fontColor_parent = self.fontColor, 
                                fontStyle_parent = self.fontStyle)
        self.moon_frame.pack(side=TOP, anchor=E, padx=self.padding_x, pady=5)
        self.moon_frame.pack_forget()
        
    def create_sunset_frame(self):
        self.sunset_frame = SunsetFrame(self.midFrame, 
                                background_parent = self.background, 
                                fontColor_parent = self.fontColor, 
                                fontStyle_parent = self.fontStyle)
        self.sunset_frame.pack(side=TOP, anchor=E, padx=self.padding_x, pady=5)
        self.sunset_frame.pack_forget()

    def create_wifi_code(self):
        self.wifi_code = WifiCodeFrame(self.midFrame, self.wifi_code_icon,
                                background_parent = self.background, 
                                fontColor_parent = self.fontColor, 
                                fontStyle_parent = self.fontStyle)
        self.wifi_code.pack(side=TOP, anchor=E, padx=self.padding_x, pady=5)
        self.wifi_code.pack_forget()
        
    def create_clock_frame(self):
        self.clock = Clock(self.topFrame, 
                        background_parent = self.background, 
                        fontColor_parent = self.fontColor, 
                        fontStyle_parent = self.fontStyle)
        self.clock.pack(side=LEFT, padx=self.padding_x, pady=self.padding_y)
    
    def create_picture_frame(self):
        self.picture_frame = PictureFrame(self.midFrame, 
                                        background_parent = self.background, 
                                        fontColor_parent = self.fontColor, 
                                        fontStyle_parent = self.fontStyle)
        self.picture_frame.pack(side=TOP)
        self.picture_frame.pack_forget()

    def create_videocamera_frame(self):
        self.videocamera_frame = VideoFrame(self.midFrame, 
                                        background_parent = self.background, 
                                        fontColor_parent = self.fontColor, 
                                        fontStyle_parent = self.fontStyle)
        self.videocamera_frame.pack(side=TOP)
        self.videocamera_frame.pack_forget()
    
    def create_calender_frame(self):            
        self.calender = Calendar(self.midFrame, self.calendar_icon,
                                background_parent = self.background, 
                                fontColor_parent = self.fontColor, 
                                fontStyle_parent = self.fontStyle)
        self.calender.pack(side=LEFT, anchor=SW, padx=self.padding_x, pady=self.padding_y)
        self.calender.pack_forget()

    def create_halloween_counter_frame(self):
        self.halloween_counter = GeneralCountdown(self.topFrame, self.holiday,
                                background_parent = self.background, 
                                fontColor_parent = self.fontColor, 
                                fontStyle_parent = self.fontStyle)
        self.halloween_counter.pack(side=RIGHT, padx=self.padding_x, pady=self.padding_y)

    def create_all_frames(self):
        self.create_clock_frame()
        self.create_weather_frame()
        self.create_moon_frame()
        self.create_sunset_frame()
        self.create_wifi_code()
        self.create_picture_frame()
        self.create_videocamera_frame()
        self.create_calender_frame()
        self.create_halloween_counter_frame()

    def update_weather(self,icon_image,new_forecast,new_temperature):
        self.weather.set_icon(icon_image)
        self.weather.set_forecast(new_forecast)
        self.weather.set_temperature(new_temperature)

    def update_moon_frame(self,icon_image,illumination,next_moon_date):
        self.moon_frame.set_icon(icon_image)
        self.moon_frame.set_illumination(illumination)
        self.moon_frame.set_nextFullMoonLbl(next_moon_date)

    def update_sunset_frame(self,icon_image,text,date):
        self.sunset_frame.set_icon(icon_image)
        self.sunset_frame.set_nextSunsetLbl(text,date)

    def show_new_slide(self,new_img):
        self.show_slides()
        self.picture_frame.show_new_slide(new_img)

    def update_events(self,new_formatted_events):
        try:
            self.show_events()
            self.calender.update_ui_events(new_formatted_events)
        except:
            print("Error on smartmirror_ui.py update_events()")

    def show_slides(self):
        if(not self.picture_frame.winfo_ismapped()):
            self.picture_frame.pack(side=TOP)

    def remove_slide_picture(self):
        self.picture_frame.pack_forget()

    def show_events(self):
        if(not self.calender.winfo_ismapped()):
            self.calender.pack(side=LEFT, anchor=SW, padx=self.padding_x, pady=self.padding_y)

    def remove_events(self):
        self.calender.pack_forget()

    def show_righ_information(self):
        if(not self.calender.winfo_ismapped()):
            self.calender.pack(side=LEFT, anchor=SW, padx=self.padding_x, pady=self.padding_y)

    def remove_extra_information(self):
        self.moon_frame.pack_forget()
        self.sunset_frame.pack_forget()
        self.wifi_code.pack_forget()

    def show_extra_information(self):
        if(not self.moon_frame.winfo_ismapped()):
            self.moon_frame.pack(side=TOP, anchor=E, padx=self.padding_x, pady=5)
        if(not self.sunset_frame.winfo_ismapped()):
            self.sunset_frame.pack(side=TOP, anchor=E, padx=self.padding_x, pady=5)
        self.wifi_code.pack(side=TOP, anchor=E, padx=self.padding_x, pady=5)
        

    def update_videocamera_photo(self,photo):
        self.videocamera_frame.update_photo(photo)

    def remove_videocamera_frame(self):
        self.videocamera_frame.pack_forget()
    
    def show_videocamera_frame(self):
        if(not self.videocamera_frame.winfo_ismapped()):
            self.videocamera_frame.pack(side=TOP)