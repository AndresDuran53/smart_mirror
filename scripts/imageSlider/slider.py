from PIL import Image, ImageTk
import tkinter as tk
import os
from os import walk

GLOBAL_PATH = "/home/pi/scripts/imageSlider/images/"

def closeLoadingScreen():
    os.system('pkill -9 -f /home/pi/scripts/loading.py')

class App(tk.Tk):
    def __init__(self, image_files, delay):
        print("Initializing App...")
        tk.Tk.__init__(self)
        self.w = self.winfo_screenwidth()
        self.h = self.winfo_screenheight()
        self.state = True
        self.attributes("-fullscreen", self.state)
        self.bg='black'
        #self.overrideredirect(1)
        #self.geometry("%dx%d+0+0" % (self.w, self.h))
        self.delay = delay
        self.pictures = []
        self.track_img_ndex = 0
        for img in image_files:
            self.pictures.append(GLOBAL_PATH+img)
        self.picture_display = tk.Label(self,bg='black')
        self.picture_display.pack(fill='both', expand=1)
        print("Initialized App")

    def show_slides(self):
        print("Showing a slide")
        self.track_img_ndex %= len(self.pictures)
        x = self.pictures[self.track_img_ndex]
        self.track_img_ndex +=1
        original_image = Image.open(x)
        original_image.thumbnail((self.w, self.h))
        #resized = original_image.resize((self.w, self.h),Image.LANCZOS)
        new_img = ImageTk.PhotoImage(original_image)
        self.picture_display.config(image=new_img,bg="black")
        self.picture_display.image = new_img
        self.title(os.path.basename(x))
        closeLoadingScreen()
        self.after(self.delay, self.show_slides)

delay = 60000


image_files = []
for (dirpath, dirnames, filenames) in walk(GLOBAL_PATH):
    image_files.extend(filenames)
    break
print(image_files)

app = App(image_files, delay)
app.show_slides()
app.mainloop()
