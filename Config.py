class Config:
    # WiFi-Einstellungen
    WIFI_SSID = "gfv-edv"  # gsog-iot
    WIFI_PASSWORD = "88DujKmT4"  # IOT_Projekt_BFK-S_2022
    
    # LED-Pin
    LED_PIN = 2
    
    # Dateipfade
    LANGZEIT_DATEI = "data/langzeitwerte.json"
    KURZZEIT_DATEI = "data/kurzzeitwerte.json"
    
    # Messwert-Limits
    MAX_LANGZEIT_WERTE = 120
    MAX_KURZZEIT_WERTE = 10
    
    # Zeitintervalle (in ms)
    LANGZEIT_INTERVALL = 3600000  
    KURZZEIT_INTERVALL = 5000     
    
    # Watchdog
    WATCHDOG_TIMEOUT = 20000  