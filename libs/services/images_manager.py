import os
import random
from PIL import Image, ImageTk

class Icons():
    global_path = "./"
    icon_folder = "assets"
    icon_lookup = {
        'Sun': "Sun.png",  # clear sky day
        'Sunrise':"Sunrise.png", # Sunrise / Sunset
        'Wind': "Wind.png",   #wind
        'Cloud': "Cloud.png",  # cloudy day
        'PartlySunny': "PartlySunny.png",  # partly cloudy day
        'Rain': "Rain.png",  # rain day
        'Snow': "Snow.png",  # snow day
        'Snow': "Snow.png",  # sleet day
        'Haze': "Haze.png",  # fog day
        'Moon': "Moon.png",  # clear sky night
        'PartlyMoon': "PartlyMoon.png",  # scattered clouds night
        'Storm': "Storm.png",  # thunderstorm
        'Tornado': "Tornado.png",    # tornado
        'Hail': "Hail.png",  # hail
        'Calendar': "calendar.png",  # hail
        'Moon0':"moon/0.png",
        'Moon1':"moon/1.png",
        'Moon2':"moon/2.png",
        'Moon3':"moon/3.png",
        'Moon4':"moon/4.png",
        'Moon5':"moon/5.png",
        'Moon6':"moon/6.png",
        'Moon7':"moon/7.png"
    }
    codes_dict = {
        "01d": "Sun",
        "01n": "Moon",
        "02d": "PartlySunny",
        "02n": "PartlyMoon",
        "03d": "Cloud",
        "03n": "Cloud",
        "04d": "Cloud",
        "04n": "Cloud",
        "09d": "Rain",
        "09n": "Rain",
        "10d": "Rain",
        "10n": "Rain",
        "11d": "Storm",
        "11n": "Storm",
        "13d": "Snow",
        "13n": "Snow",
        "50d": "Haze",
        "50n": "Haze",
        "Sunrise":'Sunrise',
        "Calendar": "Calendar",
        'Luna Nueva':"Moon0",
        'Lúnula Creciente':"Moon1",
        'Cuarto Creciente':"Moon2",
        'Gibosa Creciente':"Moon3",
        'Luna Llena':"Moon4",
        'Gibosa Menguante':"Moon5",
        'Cuarto Menguante':"Moon6",
        'Lúnula Menguante':"Moon7"
    }

    def __init__(self, global_path='./', icon_folder='assets'):
        self.global_path = global_path
        self.icon_folder = icon_folder

    def code_to_name(self, code):
        return self.codes_dict.get(code, "Sun")

    def get_icon_path_by_code(self,code):
        id = self.code_to_name(code)
        icon_path = self.icon_lookup.get(id, None)
        if(icon_path == None): return None
        return f"{self.global_path}{self.icon_folder}/{icon_path}"
    
    def get_icon_from_code(self,id, default_icon_size = 50):
        icon_path = self.get_icon_path_by_code(id)
        image = Image.open(icon_path)
        image = image.resize((default_icon_size, default_icon_size), Image.ANTIALIAS)
        image = image.convert('RGB')
        icon = ImageTk.PhotoImage(image)
        return icon

class Images():

    images_list = []

    def __init__(self, global_path='./', images_folder='scripts/imageSlider/images/'):
        self.global_path = global_path
        self.images_folder = images_folder
        self.images_list = self.get_images()
        self.next_index = 0

    def get_images(self):
        images_folder = f"{self.global_path}{self.images_folder}"
        image_files = []
        image_paths = []
        for (dirpath, dirnames, filenames) in os.walk(images_folder):
            image_files.extend(filenames)
        for img in image_files:
            image_paths.append(images_folder+img)
        random.shuffle(image_paths)
        return image_paths
    
    def get_image_from_path(self, path, width=None,height=None):
        original_image = Image.open(path)
        if(width and height): original_image.thumbnail((width, height))
        #resized = original_image.resize((self.w, self.h),Image.LANCZOS)
        return ImageTk.PhotoImage(original_image)
    
    def get_next_image(self,width=None,height=None):
        path_aux = self.images_list[self.next_index]
        self.next_index +=1
        self.next_index %= len(self.images_list)
        return self.get_image_from_path(path_aux, width, height)
        