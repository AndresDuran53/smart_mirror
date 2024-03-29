from .smartmirror_ui import FullscreenWindow

class UIController():
    def __init__(self):
        self.fullscreenWindow = FullscreenWindow()

    def set_calendar_icon(self,calendar_icon):
        self.fullscreenWindow.calendar_icon=calendar_icon

    def set_wifi_code_icon(self,wifi_code_icon):
        self.fullscreenWindow.wifi_code_icon=wifi_code_icon

    def set_next_holiday(self,holiday):
        self.fullscreenWindow.holiday=holiday

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

    def update_videocamera_photo(self,photo):
        self.fullscreenWindow.update_videocamera_photo(photo)
    
    def show_videocamera_photo(self):
        self.fullscreenWindow.show_videocamera_frame()

    def remove_videocamera_photo(self):
        self.fullscreenWindow.remove_videocamera_frame()

    def show_pictures(self):
        self.remove_events()
        self.remove_extra_information()
        self.show_picture_slide()
        self.remove_videocamera_photo()

    def show_camera(self):
        self.remove_slide_picture()
        self.remove_events()
        self.remove_extra_information()
        self.show_videocamera_photo()

    def show_information(self):
        self.remove_slide_picture()
        self.show_extra_information()
        self.remove_videocamera_photo()