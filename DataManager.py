import ujson
import time
import gc
from ZeitSpeicher import lade_zeitwerte, zeitmessung

class DataManager:
    def __init__(self, config):
        self.config = config
        
        self.langzeit_werte = None
        self.letzte_langzeit = 0
        
        self.kurzzeit_werte = None
        self.letzte_kurzzeit = 0
        
        self.init_data()
    
    def init_data(self):
        """Daten initialisieren"""
        self.langzeit_werte = lade_zeitwerte(self.config.LANGZEIT_DATEI)
        self.kurzzeit_werte = lade_zeitwerte(self.config.KURZZEIT_DATEI)
        
        current_time = time.ticks_ms()
        self.letzte_langzeit = current_time
        self.letzte_kurzzeit = current_time
    
    def should_measure_kurzzeit(self):
        """Prüfen ob Kurzzeitmessung fällig ist"""
        jetzt = time.ticks_ms()
        return time.ticks_diff(jetzt, self.letzte_kurzzeit) >= self.config.KURZZEIT_INTERVALL
    
    def should_measure_langzeit(self):
        """Prüfen ob Langzeitmessung fällig ist"""
        jetzt = time.ticks_ms()
        return time.ticks_diff(jetzt, self.letzte_langzeit) >= self.config.LANGZEIT_INTERVALL
    
    def measure_kurzzeit(self):
        """Kurzzeitmessung durchführen"""
        if zeitmessung(self.kurzzeit_werte, self.config.MAX_KURZZEIT_WERTE, self.config.KURZZEIT_DATEI):
            self.letzte_kurzzeit = time.ticks_ms()
            return True
        return False
    
    def measure_langzeit(self):
        """Langzeitmessung durchführen"""
        if zeitmessung(self.langzeit_werte, self.config.MAX_LANGZEIT_WERTE, self.config.LANGZEIT_DATEI):
            self.letzte_langzeit = time.ticks_ms()
            return True
        return False
    
    def get_langzeit_data(self):
        """Langzeit-Daten zurückgeben"""
        return self.langzeit_werte
    
    def get_kurzzeit_data(self):
        """Kurzzeit-Daten zurückgeben"""
        return self.kurzzeit_werte
    
    def update(self):
        """Daten-Update durchführen"""
        updated = False
        
        if self.should_measure_kurzzeit():
            if self.measure_kurzzeit():
                updated = True
                print("Kurzzeitmessung durchgeführt")
        
        if self.should_measure_langzeit():
            if self.measure_langzeit():
                updated = True
                print("Langzeitmessung durchgeführt")
        
        return updated
