import os
import time
import RPi.GPIO as GPIO

class FanController:
    def __init__(self, fan_pin, case_fan_pin, max_temp, mid_temp, margin_temp):
        self.fan_pin = fan_pin
        self.case_fan_pin = case_fan_pin
        self.max_temp = max_temp
        self.mid_temp = mid_temp
        self.margin_temp = margin_temp

        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.fan_pin, GPIO.OUT)
        GPIO.setup(self.case_fan_pin, GPIO.OUT)
        GPIO.setwarnings(False)            

    def get_cpu_temperature(self):
        res = os.popen('vcgencmd measure_temp').readline()
        temp = float(res.replace("temp=","").replace("'C\n",""))
        print("temp is {0}".format(temp)) #Uncomment here for testing
        return temp

    def fan_on(self, pin):
        GPIO.output(pin, True)

    def fan_off(self, pin):
        GPIO.output(pin, False)

    def set_status_by_temperature(self,fan_pin,temperature_aux,CPU_temp):
        if CPU_temp >= temperature_aux:
            self.fan_on(fan_pin)
        elif CPU_temp < (temperature_aux - self.margin_temp):
            self.fan_off(fan_pin)

    def update_fans_status(self):
        CPU_temp = self.get_cpu_temperature()
        self.set_status_by_temperature(self.case_fan_pin,self.mid_temp,CPU_temp)
        self.set_status_by_temperature(self.fan_pin,self.max_temp,CPU_temp)

cpu_fan_pin = 18
case_fan_pin = 23
max_temperature = 70
mid_temperature = 60
marginTMP = 10
fan_controller = FanController(cpu_fan_pin, case_fan_pin, max_temperature, mid_temperature, marginTMP)


delay_between_reads = 5
while True:
    fan_controller.update_fans_status()
    time.sleep(delay_between_reads) # Read the temperature every n sec