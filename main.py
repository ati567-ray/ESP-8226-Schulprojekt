import ESP8266WebServer as server
import time
import gc
from SoftwareWatchdog import SoftwareWatchdog
from Config import Config
from LEDController import LEDController
from DataManager import DataManager
from WebHandler import WebHandler
from WifiManager import WiFiManager

class TemperatureStation:
    def __init__(self):
        self.config = Config()
        self.running = False
        
        self.wifi_manager = None
        self.led_controller = None
        self.data_manager = None
        self.web_handler = None
        self.watchdog = None
    
    def init(self):
        """System initialisieren"""
        print("---------------------------- \nTemperatur-Station wird initialisiert...")
        
        self.wifi_manager = WiFiManager(self.config)
        if not self.wifi_manager.connect():
            print("Fehler: WiFi-Verbindung konnte nicht hergestellt werden!")
            return False
        
        self.led_controller = LEDController(self.config.LED_PIN)
        #Start blinker der LED
        self.led_controller.blink(3, 0.2)  
        
        self.data_manager = DataManager(self.config)
        
        self.web_handler = WebHandler(self.data_manager, self.led_controller)
        
        self._setup_webserver()
        
        self.watchdog = SoftwareWatchdog(timeout_ms=self.config.WATCHDOG_TIMEOUT)
        
        print("System erfolgreich initialisiert!")
        return True
    
    def _setup_webserver(self):
        """Webserver-Routen konfigurieren"""
        server.begin()
        server.onPath("/", self.web_handler.handle_root)
        server.onPath("/langzeitTemperatur_json", self.web_handler.handle_langzeit_temperatur)
        server.onPath("/kurzzeitTemperatur_json", self.web_handler.handle_kurzzeit_temperatur)
        server.onPath("/kurzzeitTemperatur_xml", self.web_handler.handle_xml)
        # server.onNotFound(self.web_handler.handle_not_found)
    
    def start(self):
        """Station starten"""
        if not self.init():
            return False
        
        self.running = True
        print("Temperatur-Station gestartet! \n")
        print("---------------------------- \n")
        
        try:
            self._main_loop()
        except KeyboardInterrupt:
            print("\n!---!Station durch Benutzer gestoppt!---!")
        except Exception as e:
            print(f"Fehler in der Hauptschleife: {e}")
        finally:
            self.stop()
        
        return True
    
    def _main_loop(self):
        """Hauptschleife"""
        while self.running:
            
            self.watchdog.feed()
            
            if self.data_manager.update():
                print("Messwerte aktualisiert")
            
            server.handleClient()
            
  
            self.watchdog.check()
            
            time.sleep(0.1)
        
            gc.collect()
    
    def stop(self):
        """Station stoppen"""
        self.running = False
        try:
            server.close()
        except:
            pass
        
        if self.led_controller:
            self.led_controller.blink(5, 0.1)  
        
        print("!---!Temperatur-Station gestoppt!---!was")



def main():
    """Hauptfunktion"""
    station = TemperatureStation()
    station.start()

if __name__ == "__main__":
    main()
