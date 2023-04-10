import cv2
from PIL import Image, ImageTk

class GenericCamera:
    def __init__(self, name, ip, username, password, channel):
        self.name = name
        self.ip = ip
        self.username = username
        self.password = password
        self.url = f"rtsp://{self.username}:{self.password}@{self.ip}:554/cam/realmonitor?channel={channel}&subtype=0"
        self.cap = None
    
    def connect(self):
        self.cap = cv2.VideoCapture(self.url)
        if not self.cap.isOpened():
            print("No se pudo abrir la camara")
            return False
        return True
    
    def read_frame(self):
        if(self.cap is not None):
            ret, frame = self.cap.read()
            if ret:
                return frame
        return None

    def release(self):
        if(self.cap is not None):
            self.cap.release()
            cv2.destroyAllWindows()
            self.cap = None

    def get_photo(self):
        frame_image = self.read_frame()
        if frame_image is not None:
            image = cv2.cvtColor(frame_image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            photo = ImageTk.PhotoImage(image)
            return photo
        return None

    @staticmethod
    def find_by_name(name,camera_list):
        for camera in camera_list:
            if(camera.name == name):
                return camera
        return None

    @staticmethod
    def from_json(json_config):
        name = json_config['name']
        ip = json_config['ip']
        username = json_config['username']
        password = json_config['password']
        channel = json_config['channel']
        return GenericCamera(name, ip, username, password, channel)
    
    @staticmethod
    def list_from_json(json_config):
        list_cameras_json = json_config["genericCameras"]
        final_list = []
        for camera_json in list_cameras_json:
            final_list.append(GenericCamera.from_json(camera_json))
        return final_list
    

class CameraManager:
    def __init__(self, json_config):
        self.next_index = 0
        self.actual_camera = None
        self.camera_list = GenericCamera.list_from_json(json_config)

    def move_next_index(self):
        self.next_index = (self.next_index+1)%len(self.camera_list)

    def get_next_camera(self) -> GenericCamera:
        next_camera = self.camera_list[self.next_index]
        self.move_next_index()
        print("Next Camera assigned", next_camera.name)
        return next_camera

    def next_connection(self):
        if(self.actual_camera is not None):
            self.actual_camera.release()
            print("Realising Camera", self.actual_camera.name, "to use next one")
        self.actual_camera = self.get_next_camera()
        connected = self.actual_camera.connect()
        print("Connecting to Camera", self.actual_camera.name)
        if(not connected):
            self.actual_camera = None

    def disconnect_camera(self):
        if(self.actual_camera is not None):
            self.actual_camera.release()
        self.actual_camera = None

    def get_photo(self):
        if(self.actual_camera is not None):
            return self.actual_camera.get_photo()