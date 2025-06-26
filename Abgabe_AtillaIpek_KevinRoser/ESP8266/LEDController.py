from machine import Pin
import time

class LEDController:
    def __init__(self, pin_number):
        self.led = Pin(pin_number, Pin.OUT)
        self.led.value(1)  
    
    def on(self):
        """LED einschalten"""
        self.led.value(0)
    
    def off(self):
        """LED ausschalten"""
        self.led.value(1)
    
    def blink(self, times=1, duration=0.5):
        """LED blinken lassen"""
        for _ in range(times):
            self.on()
            time.sleep(duration)
            self.off()
            time.sleep(duration)
    
    def signal_activity(self):
        """Kurzes Aktivitätssignal"""
        self.blink(1, 0.5)
