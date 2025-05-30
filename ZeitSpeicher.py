import ujson
import time
from TMP75 import read_temp  

def lade_zeitwerte(dateiname):
    try:
        with open(dateiname, "r") as f:
            return ujson.load(f)
    except Exception as e:
        print("Fehler beim Laden von", dateiname, ":", e)
        return []

def speichere_zeitwerte(werte, dateiname):
    try:
        with open(dateiname, "w") as f:
            ujson.dump(werte, f)
    except Exception as e:
        print("Fehler beim Speichern von", dateiname, ":", e)

def aktuelle_zeit_formatiert():
    ts = time.localtime()
    return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        ts[0], ts[1], ts[2], ts[3], ts[4], ts[5]
    )

def zeitmessung(liste, max_anzahl, dateiname=None):
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

