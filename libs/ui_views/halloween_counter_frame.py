from tkinter import *
from .custom_frame import CustomFrame,small_text_size,large_text_size
import time

class HalloweenCounter(Frame):
    days = ''
    default_text = "Days Until Halloween"
    icon = ''

    def __init__(self, parent, halloween_icon, **kwargs):
        CustomFrame.__init__(self, parent, kwargs)
        #Create Degree frame
        self.parentFrm = Frame(self, bg=self.background)
        self.parentFrm.pack(side=TOP, anchor=W)

        #Create Days frame
        self.countdown_label = Label(self.parentFrm, font=(self.fontStyle, large_text_size), fg=self.fontColor, bg=self.background)
        self.countdown_label.pack(side=LEFT, anchor=S)

        #Create Icon frame
        self.iconLbl = Label(self.parentFrm, bg=self.background)
        self.iconLbl.pack(side=LEFT, anchor=W, padx=20)

        #Create Text frame
        self.text_label = Label(self, text=self.default_text, font=(self.fontStyle, small_text_size), fg=self.fontColor, bg=self.background)
        self.text_label.pack(side=LEFT, anchor=S)
        self.set_icon(halloween_icon)
        self.update_countdown()

    def set_icon(self,icon_image):
        self.iconLbl.config(image=icon_image)
        self.iconLbl.image = icon_image

    def update_countdown(self):
        current_time = time.time()
        current_year = time.localtime(current_time).tm_year

        # Calculate Halloween date for the current year
        halloween_date = time.mktime(time.strptime(f"31-10-{current_year} 00:00:00", "%d-%m-%Y %H:%M:%S"))

        if current_time > halloween_date:
            # If current time is past Halloween for this year, calculate for next year
            current_year += 1
            halloween_date = time.mktime(time.strptime(f"31-10-{current_year} 00:00:00", "%d-%m-%Y %H:%M:%S"))

        time_difference = max(halloween_date - current_time, 0)

        days, seconds = divmod(time_difference, 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)

        #countdown_text = f"{int(days)} days {int(hours)} hours {int(minutes)} minutes"
        countdown_text = f"{int(days)}"
        self.countdown_label.config(text=countdown_text)

        self.after(1000, self.update_countdown)