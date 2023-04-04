import os
import time
import RPi.GPIO as GPIO


class TVController:
    def __init__(self, button_pin, red_led_pin, green_led_pin, relay_pin, sound_file):
        self.button_pin = button_pin
        self.red_led_pin = red_led_pin
        self.green_led_pin = green_led_pin
        self.relay_pin = relay_pin
        self.sound_file = sound_file
        self.setup_pins()

    def setup_pins(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.button_pin, GPIO.OUT)
        GPIO.setup(self.red_led_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.green_led_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.relay_pin, GPIO.OUT)

    def try_to_turn_on(self):
        green_led_state = GPIO.input(self.green_led_pin)
        GPIO.output(self.button_pin, GPIO.HIGH)
        var_cont = 0
        max_seconds = 20
        delay_count = 0.5
        max_count = max_seconds // delay_count 
        while (not green_led_state and var_cont < max_count):
            green_led_state = GPIO.input(self.green_led_pin)
            print("Encendido?: ", green_led_state)
            time.sleep(delay_count)
            var_cont += 1
        GPIO.output(self.button_pin, GPIO.LOW)
        time.sleep(10)
        return green_led_state

    def reproduce_sound(self):
        os.system("aplay -D hw:0,0 " + self.sound_file)

    def try_to_power_TV(self):
        print("Turning off relay")
        GPIO.output(self.relay_pin, GPIO.HIGH)
        time.sleep(30)
        print("Turning on relay")
        GPIO.output(self.relay_pin, GPIO.LOW)
        time.sleep(30)

    def check_tv_state(self):
        green_led_state = GPIO.input(self.green_led_pin)
        if (not green_led_state):
            print("No está encendido")
            red_led_state = GPIO.input(self.red_led_pin)
            if (red_led_state):
                print("Está apagado")
                green_led_state = self.try_to_turn_on()
                if green_led_state:
                    time.sleep(15)
                    self.reproduce_sound()
            else:
                print("Está desconectada")
                self.try_to_power_TV()

button_pin = 27
red_led_pin = 17
green_led_pin = 4
relay_pin = 10
tv_controller = TVController(button_pin, red_led_pin, green_led_pin, relay_pin, "/home/pi/Sounds/starting/opening2.wav")
while(1):
    tv_controller.check_tv_state()
    time.sleep(5)