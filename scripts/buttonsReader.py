import os
import time
import RPi.GPIO as GPIO

localPathImages = f"{os.path.dirname(os.path.realpath(__file__))}/"
sounds_path = f"{localPathImages}../Sounds/"

class ButtonController:
    def __init__(self, transistor_pin, button_pins):
        self.transistor_pin = transistor_pin
        self.button_pins = button_pins
        self.standby_value = 0
        self.registered_apps = [None, "Slider"]
        self.actual_app = None

        self.configure_pins()
        print("Config Done...")
        self.calibrate_buttons()
        print("Calibrated...")
        self.reset_transistor()

    def configure_pins(self):
        #GPIO.cleanup()  # cleanup all GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.transistor_pin, GPIO.OUT)
        for button_pin in self.button_pins:
            GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def get_first_button_pressed(self):
        for i, button_pin in enumerate(self.button_pins):
            if (GPIO.input(button_pin) != self.standby_value):
                self.reset_transistor()
                self.reproduce_sound()
                return i + 1
        return 0
    
    def read_all_pins(self):
        return [GPIO.input(button_pin) for button_pin in self.button_pins]
    
    def reset_transistor(self):
        GPIO.output(self.transistor_pin, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(self.transistor_pin, GPIO.HIGH)
        time.sleep(0.1)

    def calibrate_buttons(self):
        readed_value = 0
        cont = 0
        while (cont < 5):
            self.reset_transistor()
            time.sleep(1)
            results = self.read_all_pins()
            print("READERS:", results)
            if (results[0] == results[1] == results[2]):
                new_readed_value = results[0]
                if readed_value == new_readed_value:
                    cont += 1
                else:
                    readed_value = new_readed_value
                    cont = 0

    def reproduce_sound(self):
        os.system("aplay -D hw:0,0 " + sounds_path+"clicks/wooden_click.wav")

    def execute_if_pressed(self):
        pressed = self.get_first_button_pressed()
        if pressed:
            print("Button pressed:",pressed)
            if pressed == 1:
                pass
            elif pressed == 2:
                pass
            elif pressed == 3:
                pass
        return pressed

if __name__ == '__main__':
    transistor_pin = 14
    button_pins = [15, 24]
    button_controller = ButtonController(transistor_pin, button_pins)
    while(1):
        button_controller.execute_if_pressed()
        time.sleep(0.1)