import time
from tkinter import *
from .custom_frame import CustomFrame,small_text_size,large_text_size


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