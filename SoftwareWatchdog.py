import time
import machine

class SoftwareWatchdog:
    """
    Eine simple Software-basierte Watchdog-Implementierung

    Diese Klasse überwacht, ob innerhalb eines definierten Zeitlimits
    regelmäßig die "feed()"-Methode aufgerufen wird
    Wenn nicht, wird ein Neustart des Systems ausgelöst

    Attribute:
    - timeout (int): Timeout in Millisekunden
    - last_feed (int): Zeitstempel des letzten "feed()"-Aufrufs
    """

    def __init__(self, timeout_ms):
        self.timeout = timeout_ms
        self.last_feed = time.ticks_ms()

    def feed(self):
        self.last_feed = time.ticks_ms()

    def check(self):
        """
        Prüft, ob der Watchdog-Timeout überschritten wurde

        Falls der Timeout überschritten ist, wird das System neu gestartet
        """
        if time.ticks_diff(time.ticks_ms(), self.last_feed) > self.timeout:
            print("Software-Watchdog ausgelöst -> Neustart")
            machine.reset()

