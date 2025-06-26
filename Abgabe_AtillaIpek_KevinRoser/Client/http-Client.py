import http.client
import json
import time
connection = http.client.HTTPConnection('10.1.226.191', 80, timeout=10)
print(connection)

try:
    while True:
        
        
        connection.request("GET", "/api/kurzzeit")
        response = connection.getresponse()
        message = response.read()
 
        print("Status: {} and reason: {}".format(response.status, response.reason))



        text = message.decode('utf-8')


        json_object = json.loads(text)


        print(json_object)
        
        time.sleep(5)
except KeyboardInterrupt:
    print("Wurde gestoppt")


connection.close()