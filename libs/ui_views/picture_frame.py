from tkinter import *
from .custom_frame import CustomFrame

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