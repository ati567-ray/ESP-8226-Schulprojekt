import ujson
import time
from TMP75 import read_temp  

def lade_zeitwerte(dateiname):
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

def speichere_zeitwerte(werte, dateiname):
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

def aktuelle_zeit_formatiert():
    """
    Gibt die aktuelle Uhrzeit als formatierten Zeitstempel zurück

    Rückgabewert:
    - str: Zeitstempel im Format "YYYY-MM-DD HH:MM:SS"
    """
    ts = time.localtime()
    return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        ts[0], ts[1], ts[2], ts[3], ts[4], ts[5]
    )

def zeitmessung(liste, max_anzahl, dateiname=None):
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
        zeitstempel = aktuelle_zeit_formatiert()
        liste.append([zeitstempel, temperatur])
        if len(liste) > max_anzahl:
            liste.pop(0)
        speichere_zeitwerte(liste, dateiname)
        print("Wert gespeichert:", zeitstempel, temperatur)
        return True
    except Exception as e:
        print("Fehler bei Messung für", dateiname, ":", e)
        return False

