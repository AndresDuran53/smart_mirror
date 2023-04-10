from tkinter import *

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