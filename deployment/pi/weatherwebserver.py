
import http.server
import time
from datetime import datetime
import json
import serial
import board
import schedule
import sys
from multiprocessing import Process, Lock
import sched, time
import adafruit_sht31d
from adafruit_dps310.basic import DPS310
from stepperController import StepperControl
import simplejson

hostName = "weather_1"
PORT = 8080


#serial1 = serial.Serial('/dev/ttyUSB0', 9600)
serial1 = serial.Serial('/dev/ttyAMA0', 9600)

i2c = board.I2C()

humidity_s = adafruit_sht31d.SHT31D(i2c)
baro_s = DPS310(i2c)
arduino_data = {}



file1 = open("logging.log", "a")  # append mode


panmotor = StepperControl() 


def loggingWrite():
    global file1
    sensor_data = {}
    file1 = open("logging.log", "a")  # append mode
    sensor_data = gatherSensorData()
    json.dump(sensor_data, file1, indent = 6)
    file1.writelines(",")
    file1.close()


schedule.every(5).seconds.do(loggingWrite)

print("scheduled!")
#for better interrupt
def cleanup():
    print ("exiting")
    file1.close()
    sys.exit(1)

def gatherSensorData():
    sensor_data = {}
    dt = datetime.now()

    # getting the timestamp
    ts = datetime.timestamp(dt)
    try:
        #contactArduino()
        sensor_data = {
        'pressure': round(baro_s.pressure,2),
        'humidity': round(humidity_s.relative_humidity,2),
        'baro_temp': round(baro_s.temperature,2),
        'humidity_temp': round(humidity_s.temperature,2),
        #'heading': arduino_data['heading'],
        #'wind_speed': arduino_data['wind_speed'],
        'time': int(round(ts))
        }
    except ValueError:  # includes simplejson.decoder.JSONDecodeError
        print('Decoding JSON has failed')    
    #mutex!
    #lock.release()

    return sensor_data
def contactArduino():
    global arduino_data

    serial1.write(b'0')
    time.sleep(1)
    my_json = json.loads(serial1.readline().decode('utf-8'))

    arduino_data['heading'] = round(my_json.get('heading'),3)
    arduino_data['wind_speed'] = round(my_json.get('wind_speed'),3)
    time.sleep(1) 


    




class TestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        sensor_data = {}
        sensor_data = gatherSensorData()
        if self.path == '/ENVDATA':
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-type", "application/json")
            outgoing_json = json.dumps(sensor_data)
            print(outgoing_json)
            
            self.end_headers()
            self.flush_headers()
            self.wfile.write(outgoing_json.encode())
            
        if self.path == '/':
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-type", "application/json")
            print(sensor_data)
            outgoing_json = json.dumps(sensor_data)
            self.end_headers()
            self.flush_headers()

            self.wfile.write(outgoing_json.encode())

    
    def do_POST(self):

        

        self.data_string = self.rfile.read(int(self.headers['Content-Length']))

        self.send_response(200)
        self.end_headers()

        data = simplejson.loads(self.data_string)
        degreesToMove = data["degrees"]
        panmotor.move(degreesToMove, -1)


def start_server():
    """Start the server."""
    server_address = ("", PORT)
    server = http.server.HTTPServer(server_address, TestHandler)
    server.serve_forever()

def deal_with_logging():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    try:
        p = Process(target=start_server, args=())
        p.start()
        lp = Process(target=deal_with_logging, args=())
        lp.start()
        lp.join()
        p.join()
        print("good to go")

        
    except KeyboardInterrupt:
        cleanup()
