import network, utime

class WiFiManager:
    def __init__(self, config):
        self.config = config
        self.connected = False
    
    def connect(self):
        try:
            sta_if = network.WLAN(network.STA_IF)
            if not sta_if.isconnected():
                print('Verbindungsaufbau...')
                sta_if.active(True)
                sta_if.connect(self.config.WIFI_SSID, self.config.WIFI_PASSWORD)
                while not sta_if.isconnected():
                    print('.', end='')
                    utime.sleep_ms(500)
            print('\nVerbunden mit', self.config.WIFI_SSID)
            print('IP:', sta_if.ifconfig()[0])
            self.connected = True
            return True
        except Exception as e:
            print(f"WiFi-Verbindung fehlgeschlagen: {e}")
            self.connected = False
            return False

    
    def is_connected(self):
        """Status der WiFi-Verbindung"""
        return self.connected

    