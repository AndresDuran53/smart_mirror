from .smartmirror_ui import FullscreenWindow

class UIController():
    def __init__(self):
        self.fullscreenWindow = FullscreenWindow()

    def set_calendar_icon(self,calendar_icon):
        self.fullscreenWindow.calendar_icon=calendar_icon

    def create_frames(self):
        self.fullscreenWindow.create_all_frames()
    
    def execute(self):
        self.fullscreenWindow.tk.mainloop()

    def show_events(self):
        self.fullscreenWindow.show_events()

    def update_events(self,new_formatted_events):
        self.fullscreenWindow.update_events(new_formatted_events)

    def remove_events(self):
        self.fullscreenWindow.remove_events()

    def update_weather(self,icon_image,new_forecast,new_temperature):
        self.fullscreenWindow.update_weather(icon_image,new_forecast,new_temperature)

    def update_moon(self,icon_image,illumination,next_moon_date):
        self.fullscreenWindow.update_moon_frame(icon_image,illumination,next_moon_date)

    def update_sun(self,icon_image,text,date):
        self.fullscreenWindow.update_sunset_frame(icon_image,text,date)

    def show_picture_slide(self):
        self.fullscreenWindow.show_slides()

    def update_picture_slide(self,new_img):
        self.fullscreenWindow.show_new_slide(new_img)

    def remove_slide_picture(self):
        self.fullscreenWindow.remove_slide_picture()

    def show_extra_information(self):
        self.fullscreenWindow.show_extra_information()

    def remove_extra_information(self):
        self.fullscreenWindow.remove_extra_information()