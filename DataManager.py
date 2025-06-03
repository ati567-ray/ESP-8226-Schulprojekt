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

    def _messung(self, liste, max_anzahl, dateiname):
        """
        Funktion zum Erfassen und Speichern eines Temperaturwerts
        Parameter:
        - liste (list): Aktuelle Liste der Temperaturwerte (Langzeit- oder Kurzzeitmessung)
        - max_anzahl (int): Maximale Anzahl an Einträgen, die die Liste enthalten darf
        - dateiname (str): Name der lokalen JSON-Datei zur Speicherung der Daten
        Ablauf:
        - Misst die aktuelle Temperatur
        - Fügt den neuen Wert der Liste hinzu
        - Entfernt den ältesten Eintrag, falls die maximale Anzahl überschritten wird
        - Speichert die aktualisierte Liste inklusive Zeitstempel in der angegebenen JSON-Datei
        Rückgabewert:
        - True bei erfolgreicher Ausführung.
        """
        try:
            temperatur = read_temp()
            zeit = self._aktuelle_zeit()
            liste.append([zeit, temperatur])
            if len(liste) > max_anzahl:
                liste.pop(0)
            self._speichere_werte(liste, dateiname)
            print("Wert gespeichert:", zeit, ",", temperatur, "°")
            return True
        except Exception as e:
            print("Fehler bei Messung:", e)
            return False

    def should_measure_kurzzeit(self):
        """
        Überprüft ob genug Zeit seit letzter Messung vergangen ist anhand des Config KURZZEIT_INTERVALLs
        """      
        return time.ticks_diff(time.ticks_ms(), self.letzte_kurzzeit) >= self.config.KURZZEIT_INTERVALL

    def should_measure_langzeit(self):           
        """
        Überprüft ob genug Zeit seit letzter Messung vergangen ist anhand des Config LANGZEIT_INTERVALLs
        """ 
        return time.ticks_diff(time.ticks_ms(), self.letzte_langzeit) >= self.config.LANGZEIT_INTERVALL

    def measure_kurzzeit(self):
        """
        Führt die Kurzzeit-Messung aus. Setzt die Zeit neu wenn sie Erfolgreich war
        """
        if self._messung(self.kurzzeit_werte, self.config.MAX_KURZZEIT_WERTE, self.config.KURZZEIT_DATEI):
            self.letzte_kurzzeit = time.ticks_ms()
            return True
        return False

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