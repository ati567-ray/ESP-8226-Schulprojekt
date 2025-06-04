import ujson
import gc
import ESP8266WebServer as server

class WebHandler:
    def __init__(self, data_manager, led_controller):
        self.data_manager = data_manager
        self.led_controller = led_controller
    
    def get_css(self):
        """CSS-Styles zurückgeben"""
        return """
        <style>
            body {
                background-color: #cccccc;
                font-family: Arial, Helvetica, Sans-Serif;
                color: #000088;
            }
        </style>"""
    
    def handle_root(self, socket, args):
        """Root-Handler für Hauptseite"""
      
        
        page = """
        <!doctype html>
        <html lang="en">
          <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>ESP-FrontEnd</title>
            <script type="module" crossorigin src="https://ati567-ray.github.io/espfrontend/esp-frontend/dist/assets/index-98SST5nH.js"></script>
            {css}
          </head>
          <body>
              <div id="root"></div>
          </body>
        </html>
        """.format(css=self.get_css())
        

        server.ok(socket, "200", "text/html", page)
    
    def handle_langzeit_temperatur(self, socket, args):
        """Handler für Langzeit-Temperaturdaten"""
        try:
            messwerte = self.data_manager.get_langzeit_data()
            self._send_json_response(socket, messwerte)
            self.led_controller.signal_activity()
        except Exception as e:
            print("Fehler beim Lesen der Langzeit-Temperaturdaten:", e)

            server.err(socket, "500", "Fehler beim Lesen der Messwerte")
    
    def handle_kurzzeit_temperatur(self, socket, args):
        """Handler für Kurzzeit-Temperaturdaten"""
        try:
            messwerte = self.data_manager.get_kurzzeit_data()
            self._send_json_response(socket, messwerte)
            self.led_controller.signal_activity()
        except Exception as e:
            print("Fehler beim Lesen der Kurzzeit-Temperaturdaten:", e)

            server.err(socket, "500", "Fehler beim Lesen der Messwerte")
    
    def handle_xml(self, socket, args):
        """Handler für XML-Temperaturdaten"""
        try:
            messwerte = self.data_manager.get_kurzzeit_data()
            self._send_xml_response(socket, messwerte)
            self.led_controller.signal_activity()
        except Exception as e:
            print("Fehler beim Lesen der Kurzzeit-Temperaturdaten:", e)
            server.err(socket, "500", "Fehler beim Lesen der Messwerte")

    def _send_xml_response(self, socket, data):
        """XML-Response senden"""
        headers = {
            "Content-Type": "application/xml",
            "Access-Control-Allow-Origin": "*"
        }

        xml = self._list_to_xml(data)
        server.ok(socket, "200", headers, xml)
        del data
        gc.collect()

    def _list_to_xml(self, data):
        """Konvertiert die "data" Liste [zeitpunkt, temperatur] zu XML"""
        xml = "<temperaturen>"
        for eintrag in data:
            zeitpunkt, wert = eintrag
            xml += f"<eintrag><zeitpunkt>{zeitpunkt}</zeitpunkt><wert>{wert}</wert></eintrag>"
        xml += "</temperaturen>"
        return xml

    
    def _send_json_response(self, socket, data):
        """JSON-Response senden"""
        headers = {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        }

        server.ok(socket, "200", headers, ujson.dumps(data))
        del data
        gc.collect()
    
    def handle_not_found(self, socket):
        """404-Handler"""
        
        server.err(socket, "404", "File Not Found")