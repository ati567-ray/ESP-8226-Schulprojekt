from WifiConnect import wifiConnect

class WiFiManager:
    def __init__(self, config):
        self.config = config
        self.connected = False
    
    def connect(self):
        """WiFi-Verbindung herstellen"""
        try:
            wifiConnect(self.config.WIFI_SSID, self.config.WIFI_PASSWORD)
            self.connected = True
            print("WiFi erfolgreich verbunden\n")
            return True
        except Exception as e:
            print(f"WiFi-Verbindung fehlgeschlagen: {e}\n")
            self.connected = False
            return False
    
    def is_connected(self):
        """Status der WiFi-Verbindung"""
        return self.connected