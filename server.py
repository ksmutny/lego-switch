from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from PCA9685 import PCA9685


pwm = PCA9685(0x40)
pwm.setPWMFreq(50)

initial_positions = [1500, 1500, 1500, 1500,
                     1500, 1500, 1500, 1500,
                     1500, 1500, 1500, 1500,
                     1500, 1500, 1500, 1500]

DELTA_OFF = 220


def initialize_servos():
    global pwm, initial_positions
    for id in range(0, 16):
        pwm.setServoPulse(id, initial_positions[id])


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

        if 'calibrate' in content:
            initial_positions[id] = content['calibrate']
            self.set_switch_position(id, on = True)

        if 'on' in content:
            self.set_switch_position(id, content['on'])

        self.send_response(201)
        self.end_headers()

    def set_switch_position(self, id, on):
        position = initial_positions[id] + (0 if on else DELTA_OFF)
        print('Switch', id, 'on' if on else 'off', 'at position', position)
        pwm.setServoPulse(id, position)

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
