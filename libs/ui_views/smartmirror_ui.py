import time
from tkinter import *

large_text_size = 40
medium_text_size = 26
small_text_size = 20
title_event_text_size = 18
event_text_size =16

class CustomFrame(Frame):
    def __init__(self,parent,extra_args):
        self.background = extra_args["background_parent"]
        self.fontColor = extra_args["fontColor_parent"]
        self.fontStyle = extra_args["fontStyle_parent"]
        Frame.__init__(self, parent, bg=self.background)

class Clock(CustomFrame):
    time_saved = ''
    date_saved = ''
    day_of_week = ''

    def __init__(self, parent, *args, **kwargs):
        CustomFrame.__init__(self, parent, kwargs)
        # initialize time label
        self.timeLbl = Label(self, text=self.time_saved, font=(self.fontStyle, large_text_size), fg=self.fontColor, bg=self.background)
        self.timeLbl.pack(side=TOP, anchor=E)
        # initialize date label
        self.dateLbl = Label(self, text=self.date_saved, font=(self.fontStyle, small_text_size), fg=self.fontColor, bg=self.background)
        self.dateLbl.pack(side=RIGHT)
        # initialize day of week
        self.dayOWLbl = Label(self, text=self.day_of_week, font=(self.fontStyle, small_text_size), fg=self.fontColor, bg=self.background)
        self.dayOWLbl.pack(side=RIGHT)
        self.tick()

    def get_local_datetime(self,timeFormat=24):
        if timeFormat == 12:
            date_format = "%I:%M:%p %A %d/%b/%Y"  # hour in 12h format
        else:
            date_format = "%H:%M %A %d/%b/%Y"  # hour in 24h format

        local_time = time.strftime(date_format)
        new_time, new_day_of_week, new_date = local_time.split()
        new_day_of_week = self.translate_day(new_day_of_week)
        new_date = " ".join(new_date.split("/"))
        return new_time, new_day_of_week, new_date
    
    def translate_day(self,day_name):
        days_spanish = {
            "monday": "Lunes",
            "tuesday": "Martes",
            "wednesday": "Miercoles",
            "thursday": "Jueves",
            "friday": "Viernes",
            "saturday": "Sabado",
            "sunday": "Domingo"
        }
        new_day_name = days_spanish.get(day_name.lower(), day_name)
        return new_day_name

    def updateUI(self):
        self.timeLbl.config(text=self.time_saved)
        self.dayOWLbl.config(text=self.day_of_week+" ")
        self.dateLbl.config(text=self.date_saved)

    def tick(self):
        try:
            new_time, new_day_of_week, new_date = self.get_local_datetime(12)
            self.time_saved = new_time
            self.day_of_week = new_day_of_week
            self.date_saved = new_date
            self.updateUI()
        except Exception as e:
            print("Error (log): Actualizar Hora: "+ str(e))
        self.timeLbl.after(1000, self.tick)


class Calendar(Frame):
    calendar_icon = None
    formatted_events=None
    last_owner = ""

    def __init__(self, parent, calendar_icon, **kwargs):
        CustomFrame.__init__(self, parent, kwargs)
        self.calendarEventContainer = Frame(self, bg=self.background)
        self.calendarEventContainer.pack(side=BOTTOM, anchor=W)
        self.calendar_icon = calendar_icon
        

    def create_calendar_event(self,event):
        calendar_event = CalendarEvent(self.calendarEventContainer,self.calendar_icon,
                                        background_parent = self.background, 
                                        fontColor_parent = self.fontColor, 
                                        fontStyle_parent = self.fontStyle)
        calendar_event.eventTitleLbl.config(text=event.get_title())
        calendar_event.eventNameLbl.config(text=event.get_time())
        return calendar_event

    def remove_all_events(self):
        for widget in self.calendarEventContainer.winfo_children():
            widget.destroy()
        self.last_owner=""
    
    def show_event_list(self):
        list_frame_events = []
        for event in self.formatted_events:
            calendarLbl = self.change_calendar_owner(event.owner_name)
            if(calendarLbl is not None): list_frame_events.append((calendarLbl,(8, 0)))
            calendar_event = self.create_calendar_event(event)
            list_frame_events.append((calendar_event,8))
        for frame_event,padding_y in list_frame_events:
                    frame_event.pack(side=TOP, anchor=W, pady=padding_y)

    def update_ui_events(self,new_formatted_events):
        if(self.formatted_events != new_formatted_events or len(self.calendarEventContainer.winfo_children())==0):
            self.formatted_events = new_formatted_events
            self.remove_all_events()
            if(len(self.formatted_events)>0):
                self.show_event_list()
            else:
                calendar_event = CalendarEvent(self.calendarEventContainer,self.calendar_icon,
                                        background_parent = self.background, 
                                        fontColor_parent = self.fontColor, 
                                        fontStyle_parent = self.fontStyle)
                calendar_event.eventTitleLbl.config(text="Sin acceso al calendario de eventos")
                calendar_event.pack(side=TOP, anchor=W, pady=8)

    def change_calendar_owner(self,owner):
        if(self.last_owner==owner): return None
        self.last_owner=owner
        text = F"{owner} events:"
        calendarLbl = Label(self.calendarEventContainer, text=text, font=(self.fontStyle, small_text_size), fg="#79D9D4", bg=self.background)
        return calendarLbl

class CalendarEvent(Frame):
    def __init__(self, parent, calendar_icon, event_name="Ningun evento registrado", **kwargs):
        CustomFrame.__init__(self, parent, kwargs)
        self.iconLbl = Label(self, bg=self.background, image=calendar_icon)
        self.iconLbl.image = calendar_icon
        self.iconLbl.pack(side=LEFT, anchor=N)
        self.eventName = event_name
        self.eventTitleLbl = Label(self, text="Prueba de titulo", font=(self.fontStyle, title_event_text_size), fg=self.fontColor, bg=self.background)
        self.eventTitleLbl.pack(side=TOP, anchor=W)
        self.eventNameLbl = Label(self, text=self.eventName, font=(self.fontStyle, event_text_size), fg="#AAAAAA", bg=self.background)
        self.eventNameLbl.pack(side=TOP, anchor=W)


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
        # remove image
        #self.iconLbl.config(image='')

    def set_forecast(self,new_forecast):
        if self.forecast != new_forecast:
            self.forecast = new_forecast
            self.forecastLbl.config(text=new_forecast)

    def set_temperature(self,new_temperature):
        if self.temperature != new_temperature:
            self.temperature = new_temperature
            self.temperatureLbl.config(text=new_temperature)


class PictureFrame(CustomFrame):
    def __init__(self, parent, **kwargs):
        CustomFrame.__init__(self, parent, kwargs)
        self.create_widget()
        
    def show_new_slide(self,new_img):
        try:
            self.picture_display.config(image=new_img,bg=self.background)
            self.picture_display.image = new_img
        except:
            self.create_widget()
            self.picture_display.config(image=new_img,bg=self.background)

    def create_widget(self):
        self.picture_display = Label(self,bg=self.background)
        self.picture_display.pack(fill='both', expand=1)
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

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
    
    def create_calender_frame(self):            
        self.calender = Calendar(self.midFrame, self.calendar_icon,
                                background_parent = self.background, 
                                fontColor_parent = self.fontColor, 
                                fontStyle_parent = self.fontStyle)
        self.calender.pack(side=LEFT, anchor=SW, padx=self.padding_x, pady=self.padding_y)
        self.calender.pack_forget()

    def create_all_frames(self):
        self.create_clock_frame()
        self.create_weather_frame()
        self.create_moon_frame()
        self.create_sunset_frame()
        self.create_picture_frame()
        self.create_calender_frame()

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
        self.show_events()
        self.calender.update_ui_events(new_formatted_events)

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

    def show_extra_information(self):
        if(not self.moon_frame.winfo_ismapped()):
            self.moon_frame.pack(side=TOP, anchor=E, padx=self.padding_x, pady=5)
        if(not self.sunset_frame.winfo_ismapped()):
            self.sunset_frame.pack(side=TOP, anchor=E, padx=self.padding_x, pady=5)