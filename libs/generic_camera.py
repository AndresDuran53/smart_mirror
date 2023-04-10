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
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()

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