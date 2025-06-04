# data_manager.py

import ujson
import time
import gc
from TMP75 import read_temp

class DataManager:
    def __init__(self, config):
        self.config = config
        self.langzeit_werte = self._lade_werte(config.LANGZEIT_DATEI)
        self.kurzzeit_werte = self._lade_werte(config.KURZZEIT_DATEI)
        now = time.ticks_ms()
        self.letzte_langzeit = now
        self.letzte_kurzzeit = now

    def _lade_werte(self, dateiname):
        """
        Lädt eine Liste von Zeitwerten aus einer lokalen JSON-Datei

        Parameter:
        - dateiname (str): Name der JSON-Datei, aus der die Werte geladen werden sollen

        Rückgabewert:
        - list: Geladene Liste von Zeitwerten (leere Liste bei Fehler)
        """
        try:
            with open(dateiname, "r") as f:
                return ujson.load(f)
        except Exception as e:
            print("Fehler beim Laden von", dateiname, ":", e)
            return []

    def _speichere_werte(self, werte, dateiname):
        """
        Speichert eine Liste von Zeitwerten in eine lokale JSON-Datei

        Parameter:
        - werte (list): Liste der zu speichernden Zeit-Temperatur-Werte
        - dateiname (str): Name der JSON-Datei, in der die Werte gespeichert werden sollen
        """
        try:
            with open(dateiname, "w") as f:
                ujson.dump(werte, f)
        except Exception as e:
            print("Fehler beim Speichern von", dateiname, ":", e)

    def _aktuelle_zeit(self):
        """
        Gibt die aktuelle Uhrzeit als formatierten Zeitstempel zurück

        Rückgabewert:
        - str: Zeitstempel im Format "YYYY-MM-DD HH:MM:SS"
        """
        ts = time.localtime()
        return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
            ts[0], ts[1], ts[2], ts[3], ts[4], ts[5]
        )
  
    def should_measure(self, last_time, interval):
        
        """
        Überprüft, ob seit der letzten Messung genügend Zeit vergangen ist

        Parameter:
        - last_time (int): Zeitstempel der letzten Messung in Millisekunden 
        - interval (int): Zeitintervall in Millisekunden

        Rückgabewert:
        - True, wenn das definierte Intervall überschritten wurde
        - False, wenn das Intervall noch nicht erreicht wurde
        """
        return time.ticks_diff(time.ticks_ms(), last_time) >= interval

      def measure(self, werte_liste, max_werte, datei, last_time_attr):
        """
        Führt eine Temperaturmessung durch, speichert den Wert in der JSON-Datei
        und aktualisiert den Zeitstempel bei erfolgreicher Ausführung.

        Parameter:
        - werte_liste (list): Liste für die aktuellen Messwerte
        - max_werte (int): Maximale Anzahl an Einträgen 
        - datei (str): Ziel-JSON-Datei
        - last_time_attr (str): Name des Attributs, das den letzten Zeitstempel hält
        
        Rückgabewert:
        - True bei Erfolg, False bei Fehler
        """
        try:
            temperatur = read_temp()
            zeit = self._aktuelle_zeit()
            werte_liste.append([zeit, temperatur])
            if len(werte_liste) > max_werte:
                werte_liste.pop(0)
            self._speichere_werte(werte_liste, datei)
            setattr(self, last_time_attr, time.ticks_ms()) # dynamisch Attribut zu setzen
            print("Wert gespeichert:", zeit, ",", temperatur, "°")
            return True
        except Exception as e:
            print("Fehler bei Messung:", e)
            return False

    def update(self):
        """Daten-Update durchführen"""
        updated = False
        
        # Kurzzeitmessung
        if self.should_measure(self.letzte_kurzzeit, self.config.KURZZEIT_INTERVALL):
            if self.measure(self.kurzzeit_werte, self.config.MAX_KURZZEIT_WERTE, 
                           self.config.KURZZEIT_DATEI, 'letzte_kurzzeit'):
                updated = True
                print("Kurzzeitmessung durchgeführt")
        
        # Langzeitmessung  
        if self.should_measure(self.letzte_langzeit, self.config.LANGZEIT_INTERVALL):
            if self.measure(self.langzeit_werte, self.config.MAX_LANGZEIT_WERTE,
                           self.config.LANGZEIT_DATEI, 'letzte_langzeit'):
                updated = True
            print("Langzeitmessung durchgeführt")
    

    def measure_langzeit(self):
        """
        Führt die Langzeit-Messung aus. Setzt die Zeit neu wenn sie Erfolgreich war
        """
        if self._messung(self.langzeit_werte, self.config.MAX_LANGZEIT_WERTE, self.config.LANGZEIT_DATEI):
            self.letzte_langzeit = time.ticks_ms()
            return True
        return False

    def get_kurzzeit_data(self):
        return self.kurzzeit_werte

    def get_langzeit_data(self):
        return self.langzeit_werte

    