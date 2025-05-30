import time
import machine

class SoftwareWatchdog:
    def __init__(self, timeout_ms):
        self.timeout = timeout_ms
        self.last_feed = time.ticks_ms()

    def feed(self):
        self.last_feed = time.ticks_ms()

    def check(self):
        if time.ticks_diff(time.ticks_ms(), self.last_feed) > self.timeout:
            print("Software-Watchdog ausgelöst → Neustart")
            machine.reset()

