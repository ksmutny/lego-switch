from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from PCA9685 import PCA9685


pwm = PCA9685(0x40)
pwm.setPWMFreq(50)

POS_INIT = 1500
POS_ON = POS_INIT
POS_OFF = 2200


def initialize_servos():
    global pwm
    for id in range(0, 16):
        pwm.setServoPulse(id, POS_INIT)


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        global pwm

        content_type = self.headers['Content-Type']
        content_length = int(self.headers['Content-Length'])

        if content_type != 'application/json':
            self.send_bad_request()
            return

        content = json.loads(self.rfile.read(content_length))
        id = content['id']
        on = content['on']

        print('Switching switch', id, 'on' if on else 'off')
        pwm.setServoPulse(id, POS_ON if on else POS_OFF)

        self.send_response(201)
        self.end_headers()

    def send_bad_request(self):
        self.send_response(400)
        self.end_headers()



def start_server():
    port = 8000
    conf = ('', port)
    server = HTTPServer(conf, RequestHandler)
    print('Started HTTP server at port', port)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()
    print('Closed HTTP server at port', port)


initialize_servos()
start_server()
