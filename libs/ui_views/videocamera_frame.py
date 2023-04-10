from tkinter import *
from .custom_frame import CustomFrame

class VideoFrame(CustomFrame):
    def __init__(self, parent, **kwargs):
        CustomFrame.__init__(self, parent, kwargs)
        self.create_widget()

    def create_widget(self):
        self.label = Label(self)
        self.label.pack(fill='both', expand=1)

    def update_photo(self,photo):
        self.label.config(image=photo)
        self.label.image = photo