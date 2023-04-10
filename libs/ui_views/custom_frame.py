from tkinter import *

large_text_size = 40
medium_text_size = 26
small_text_size = 20
title_event_text_size = 18
event_text_size =16

class CustomFrame(Frame):
    def __init__(self,parent,extra_args):
        try:
            self.background = extra_args["background_parent"]
            self.fontColor = extra_args["fontColor_parent"]
            self.fontStyle = extra_args["fontStyle_parent"]
        except:
            self.background = "black"
            pass
        Frame.__init__(self, parent, bg=self.background)