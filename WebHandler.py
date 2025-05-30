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
        temperature = self.data_manager.get_current_temperature()
        
        page = """
        <!doctype html>
        <html lang="en">
          <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>ESP-FrontEnd</title>
            <script type="module" crossorigin src="https://ati567-ray.github.io/test123/index-DCcrAdFN.js"></script>
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