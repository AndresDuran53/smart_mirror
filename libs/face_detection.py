import cv2
import psutil
import time
from datetime import datetime
import os
from .smartmirror_utils import log

class VideoCapture:
    def __init__(self, source, width, height):
        self.width = width
        self.height = height
        self.source = source
        self.create_cap()

    def create_cap(self):
        self.cap = cv2.VideoCapture(self.source)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        time.sleep(2)

    def delete(self):
        self.cap.release()
        self.cap = None

    def get_frame(self):
        if(self.cap == None):
            self.create_cap()
        ret, frame = self.cap.read()
        if ret:
            return cv2.resize(frame, (self.width, self.height))
        else:
            return None

class FaceDetector:
    def __init__(self, xml_file_path, scale_factor=1.1, min_neighbors=6, min_size=(40, 40), flags=cv2.CASCADE_SCALE_IMAGE, percent_to_detect=0.25, min_constant_face_counter=3):

        localPathImages = f"{os.path.dirname(os.path.realpath(__file__))}/"

        self.face_cascade = cv2.CascadeClassifier(localPathImages+xml_file_path)
        self.scale_factor = scale_factor
        self.min_neighbors = min_neighbors
        self.min_size = min_size
        self.flags = flags
        self.percent_to_detect = percent_to_detect
        self.min_constant_face_counter = min_constant_face_counter
        self.face_timer = 0

    def detect_faces(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=self.scale_factor, minNeighbors=self.min_neighbors, minSize=self.min_size, flags=self.flags)
        close_detected_faces = self.get_close_detected_faces(faces,frame)
        if(self.faces_count_verification(close_detected_faces)):
            return close_detected_faces
        else: return []

    def get_minimun_face_margin(self,camera_size,face_size):
        extra_size = camera_size - face_size
        margin_size = extra_size/4
        return margin_size
    
    def get_close_detected_faces(self,faces,frame):
        close_detected_faces = []
        for (x, y, w, h) in faces:
            if ((w > frame.shape[1]*self.percent_to_detect) or (h > frame.shape[0]*self.percent_to_detect)):
                width_minimun_margin = self.get_minimun_face_margin(frame.shape[1],w)
                if(x >= width_minimun_margin and (x+w <= frame.shape[1]-width_minimun_margin)):
                    close_detected_faces.append((x, y, w, h,(0, 255, 0)))
        return close_detected_faces
    
    def faces_count_verification(self,close_detected_faces):
        if (len(close_detected_faces) > 0): 
            self.face_timer += 1
        else: 
            self.face_timer = 0
        return (self.face_timer >= self.min_constant_face_counter)


class FaceDetectorApp:
    def __init__(self, source=0, width=320, height=240):
        self.video_capture = VideoCapture(source, width, height)
        self.face_detector = FaceDetector('haarcascade_frontalface_default.xml')
        self.cpu_delay_counter = 0
        self.no_face_counter = 10
        self.face_counter_delay = 8
        self.is_new_person_detected = False

    def run(self):
        try:
            frame = self.video_capture.get_frame()
            if frame is None: 
                self.is_new_person_detected = False
                return
            faces = self.face_detector.detect_faces(frame)
            person_detected_old = self.is_new_person_detected
            self.is_new_person_detected = self.is_person_detected(faces)
            if(self.is_new_person_detected and person_detected_old != self.is_new_person_detected):
                self.save_face_image(frame,faces)
            #self.monitor_cpu()
            if cv2.waitKey(1) & 0xFF == ord('q'): return
            cv2.setWindowProperty('Video', cv2.WND_PROP_VSYNC, 0)
        except Exception as e:
            log("Error: Cannot get frame for face recognition. " + str(e))
            self.video_capture.delete()
            cv2.destroyAllWindows()
            self.is_new_person_detected = False

    def is_person_detected(self,faces):
        is_there_faces = len(faces)>0
        self.no_face_counter = 0 if is_there_faces else self.no_face_counter + 1
        return (self.no_face_counter < self.face_counter_delay)

    def monitor_cpu(self):
        self.cpu_delay_counter += 1
        if (self.cpu_delay_counter < 5): return
        cpu_usage = psutil.cpu_percent()
        print(f"Uso de CPU: {cpu_usage}%")
        self.cpu_delay_counter = 0

    def draw_faces(self,frame,faces):
        for (x, y, w, h, color) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        return frame

    def save_face_image(self,frame,faces):
        frame = self.draw_faces(frame,faces)
        localPathImages = f"{os.path.dirname(os.path.realpath(__file__))}/"
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
        file_name = f"{localPathImages}face-{dt_string}.jpg"
        cv2.imwrite(file_name, frame)

if __name__ == '__main__':
    app = FaceDetectorApp()
    app.run()