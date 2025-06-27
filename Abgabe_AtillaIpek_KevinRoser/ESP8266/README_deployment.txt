Alle ESP-Dateien so wie sie sind auf geflasheten ESP uploaden.
Speichern.

__________________________________________________________

WLAN-Zugang (SSID/Passwort in Config.py konfigurierbar) -

Beim Neustart wird boot.py automatisch ausgeführt und ruft main.main() auf -


Nach erfolgreichem Start verbindet sich das Gerät mit dem in Config.py konfigurierten WLAN und der Webserver ist dann im gleichen Netzwerk auch ansprechbar.
__________________________________________________________

Verfügbare Endpunkte:

*/ – Root-Seite

*/api/langzeit – Langzeitdaten als JSON

*/api/kurzzeit – Kurzzeitdaten als JSON

*/api/xml – Temperaturdaten im XML-Format
__________________________________________________________

Konfigurierbare Parameter (aus Config.py)

WIFI_SSID	WLAN-Name	"xxx"
WIFI_PASSWORD	WLAN-Passwort	"xxx"
LED_PIN	Pin für Status-LED	2
LANGZEIT_INTERVALL	Intervall für Langzeitmessung (ms)	3600000
KURZZEIT_INTERVALL	Intervall für Kurzzeitmessung (ms)	5000
WATCHDOG_TIMEOUT	Timeout für Software-Watchdog (ms)	20000

__________________________________________________________


Hinweise!!!
Wenn keine WLAN-Verbindung möglich ist, startet der Webserver nicht.

Wenn kein Internetzugang vorhanden ist oder der Link outdated ist wird das Frontend nicht funktionieren. (Im WebHandler.py der Link)

Die LED blinkt beim Startvorgang zur Bestätigung.

Fehlerhafte Zustände werden über den Watchdog erkannt.
__________________________________________________________
