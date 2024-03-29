import os
import gc
from libs.iterated_thread import IteratedThreadWithDelay
from libs.ui_views.ui_controller import UIController
from libs.events_manager import EventHandler
from libs.services.images_manager import Icons,Images
from libs.services.openweathermap_service import OpenWeatherMap
from libs.services.mqtt_controller import MqttController, MqttConfig
from libs.configuration_reader import ConfigurationReader
from libs.smartmirror_utils import log
from libs.face_detection import FaceDetectorApp
from libs.celestial_body_viewer import CelestialBodyViewer
from libs.generic_camera import CameraManager
from libs.ui_views.countdown.holiday import Holiday

try:
    from scripts.buttonsReader import ButtonController
    is_raspberry_pi = True
except:
    is_raspberry_pi = False
    print("Is not on a Raspberry Pi")

class Application:
    is_person_detected = False
    has_show_information = False
    has_to_show_camera = False
    stored_events = []

    def __init__(self):
        
        #Creating Configuration object
        localPathImages = f"{os.path.dirname(os.path.realpath(__file__))}/"
        config_data = ConfigurationReader.read_config_file(localPathImages)
        
        #Creating Mqtt objects
        self.connectMqtt(config_data)

        #Create Camera Objects
        self.camera_manager = CameraManager(config_data)

        #Creating UI object
        self.ui_controller = UIController()
        #Creating Face Recognition
        self.face_recognition = FaceDetectorApp("http://192.168.0.4:8581/")
        #Creating Service objects
        self.openweathermap_manager = OpenWeatherMap.from_json(config_data)
        self.event_handler = EventHandler(config_data)
        self.icon_manager = Icons(localPathImages)
        self.image_manager = Images(localPathImages)

        #Creating Moon calculador
        self.celestial_body_viewer = CelestialBodyViewer()

        #Creating ButtonController
        self.create_button_controller()

        #Getting UI Values
        calendar_icon = self.icon_manager.get_icon_from_code("Calendar",default_icon_size = 26)
        wifi_code_icon = self.icon_manager.get_icon_from_code("WifiCodeIcon",default_icon_size = 200)
        halloween_icon = self.icon_manager.get_icon_from_code("Halloween",default_icon_size = 125)

        #Setting UI values
        self.get_screen_dimensions()
        self.ui_controller.set_calendar_icon(calendar_icon)
        self.ui_controller.set_wifi_code_icon(wifi_code_icon)
        self.ui_controller.set_next_holiday(Holiday("Halloween","31-10",halloween_icon))

        #Creating UI frames
        self.ui_controller.create_frames()

        #Updating UI values first time
        #self.update_weather()
        self.update_general_information()
        #self.has_show_information = True
        #self.camera_manager.next_index = 2
        #self.set_new_camera_to_show()
        self.update_screen_showing_frames()

    def connectMqtt(self,config_data):
        try:
            mqtt_config = MqttConfig.from_json(config_data)
            self.mqtt_controller = MqttController(mqtt_config,self.on_message,"SmartMirror")
            self.topic_state_pub = mqtt_config.person_detected_topic
            self.mqttConnected = True
        except:
            self.mqttConnected = False

    def create_button_controller(self):
        if(is_raspberry_pi):
            transistor_pin = 14
            button_pins = [15, 24, 25]
            self.button_controller = ButtonController(transistor_pin, button_pins)


    def get_screen_dimensions(self):
        self.screen_width = self.ui_controller.fullscreenWindow.tk.winfo_screenwidth()
        self.screen_height = self.ui_controller.fullscreenWindow.tk.winfo_screenheight()
                
    def update_events(self):
        print("Updating Events...")
        formatted_events=[]
        try:
            formatted_events = self.event_handler.get_event_list()
        except Exception as e:
            log("Error: Cannot get calendar. " + str(e))
        if(self.stored_events != formatted_events):
            self.stored_events = formatted_events

    def update_weather(self):
        print("Updating Weather...")
        try:
            weather_obj = self.openweathermap_manager.get_weather()
            actual_temperature = self.openweathermap_manager.get_temperatur_from_obj(weather_obj)
            forecast = self.openweathermap_manager.get_forecast_from_obj(weather_obj)
            icon_id = self.openweathermap_manager.get_icon_id_from_obj(weather_obj)
            icon_image = self.icon_manager.get_icon_from_code(icon_id)
            self.ui_controller.update_weather(icon_image,forecast,actual_temperature)
        except Exception as e:
            log("Error: Cannot get weather. " + str(e))

    def update_moon(self):
        moon_phase_value = self.celestial_body_viewer.get_moon_phase()
        moon_phase = f"{int(round(moon_phase_value, 2)*100)}%"
        moon_phase_name = self.celestial_body_viewer.get_name_moonphase(moon_phase_value)
        icon_image = self.icon_manager.get_icon_from_code(moon_phase_name)
        next_moon_date = self.celestial_body_viewer.get_next_full_moon()
        self.ui_controller.update_moon(icon_image,moon_phase,next_moon_date)

    def update_sun(self):
        text,date = self.celestial_body_viewer.get_next_sun_event()
        icon_image = self.icon_manager.get_icon_from_code("Sunrise")
        self.ui_controller.update_sun(icon_image,text,date)

    def show_next_picture_slide(self):
        if(self.has_show_information or self.has_to_show_camera): return
        try:
            width = self.screen_width*0.9
            height = self.screen_height*0.8
            new_image = self.image_manager.get_next_image(width, height)
            self.ui_controller.update_picture_slide(new_image)
            gc.collect()
        except Exception as e:
            log("Error: Cannot update picture slide. " + str(e))

    def update_videoframe(self):
        if(self.has_to_show_camera):
            try:
                photo = self.camera_manager.get_photo()
                if(photo is not None):
                    self.ui_controller.update_videocamera_photo(photo)
                    gc.collect()
            except Exception as e:
                log("Unable to update videoframe: " + str(e))

    def update_general_information(self):
        self.update_events()
        self.show_next_picture_slide()
        self.update_moon()
        self.update_sun()
        self.send_temp_update()

    def update_screen_showing_frames(self):
        if(self.has_to_show_camera):
            self.ui_controller.show_camera()
        elif(self.has_show_information):
            self.ui_controller.update_events(self.stored_events) 
            self.ui_controller.show_information()
        else:
            self.ui_controller.show_pictures()

    def send_temp_update(self):
        if(is_raspberry_pi):
            try:
                res = os.popen('vcgencmd measure_temp').readline()
                temp = str(float(res.replace("temp=","").replace("'C\n","")))
                self.communicate_value("smartmirror/state/temperature",temp)
            except:
                pass
                      
    def execute_face_recognition(self):
        try:
            self.face_recognition.run()
            new_person_detected = self.face_recognition.is_new_person_detected
            if(self.is_person_detected != new_person_detected):
                log("Face Recognition Is Different")
                self.is_person_detected = new_person_detected
                self.has_show_information = self.is_person_detected
                if(self.has_show_information):
                    self.communicate_value(self.topic_state_pub,"1")
                    pass
                else:
                    self.communicate_value(self.topic_state_pub,"0")
                    pass
                self.update_screen_showing_frames()     
        except Exception as e:
            log("Error: Cannot execute face recognition. " + str(e))

    def read_buttons(self):
        value = self.button_controller.execute_if_pressed()
        if(value == 0): return
        elif(value == 1):
            self.set_new_camera_to_show()
            self.update_screen_showing_frames()
        elif(value == 2):
            self.disconnect_showing_camera()
            self.update_screen_showing_frames()
        elif(value == 3):
            self.communicate_value("smartmirror/request/lights","change")
        self.communicate_value("smartmirror/button/pressed",str(value))

    def set_new_camera_to_show(self):
        self.camera_manager.next_connection()
        self.has_to_show_camera = True

    def disconnect_showing_camera(self):
        self.has_to_show_camera = False
        self.camera_manager.next_index = 0
        self.ui_controller.update_videocamera_photo(None)

    def communicate_value(self,topic,value):
        if(self.mqttConnected):
            self.mqtt_controller.send_message(topic,value)
        else:
            log("Mqtt is not connected")

    def on_message(self,client, userdata, message):
        message_recieved = str(message.payload.decode("utf-8"))
        topic = message.topic
        log(f"[New Mqtt Message] Topic: {topic} | Message: {message_recieved}")
        if("smartmirror/event/add" == topic):
            self.ui_controller.update_events([message_recieved])

    def run_ui_mainloop(self):
        try:
            self.ui_controller.execute()
        except Exception as e:
            log("MainException: "+str(e))

if __name__ == '__main__':
    app = Application()

    thread_events_update = IteratedThreadWithDelay(app.update_general_information,300)
    thread_events_update.start()

    #thread_weather_update = IteratedThreadWithDelay(app.update_weather,3600)
    #thread_weather_update.start()

    thread_face_recognition = IteratedThreadWithDelay(app.execute_face_recognition,0.3)
    thread_face_recognition.start()

    if(is_raspberry_pi):
        thread_button_reader = IteratedThreadWithDelay(app.read_buttons,0.1)
        thread_button_reader.start()

    thread_videocamera_view = IteratedThreadWithDelay(app.update_videoframe,0.1)
    thread_videocamera_view.start()

    app.run_ui_mainloop()