import time
import threading

class IteratedThreadWithDelay():
    def __init__(self,repetitive_method,seconds_delay):
        self.repetitive_method = repetitive_method
        self.seconds_delay = seconds_delay
        self.repetitive_thread = threading.Thread(target=self.execute, daemon=True)

    def execute(self):
        while True:
            self.repetitive_method()
            time.sleep(self.seconds_delay)

    def start(self):
        self.repetitive_thread.start()