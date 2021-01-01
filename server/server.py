from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from switch import calibrate_switch, set_switch_position, get_switch_position, Position

POSITION_VALUE = {
    'on': Position.ON,
    'off': Position.OFF
}


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        command = self.validate_payload()
        if isinstance(command, str):
            error_message = command
            print('Bad request:', error_message)
            return self.send_bad_request(error_message)

        port = command['port']

        if 'calibrate' in command:
            offset = command['calibrate']
            calibrate_switch(port, offset)
            print('Calibrated switch', port, 'to', offset)

        if 'position' in command:
            position = POSITION_VALUE[command['position']]
            set_switch_position(port, position)
            print('Switched', port, 'to', position)

        self.send_response(201)
        self.end_headers()


    def validate_payload(self):
        content_type = self.headers['Content-Type']
        content_length = int(self.headers['Content-Length'])

        if content_type != 'application/json':
            return 'Not JSON payload'

        content = json.loads(self.rfile.read(content_length))

        print(content)

        if 'port' not in content or not isinstance(content['port'], int):
            return 'Missing "port" attribute, or "port" not a number.'

        if 'calibrate' not in content and 'position' not in content:
            return 'Invalid command. Use "calibrate" or "position".'

        if 'calibrate' in content and not isinstance(content['calibrate'], int):
            return 'Attribute "calibrate" not a number.'

        if 'position' in content and content['position'] not in POSITION_VALUE:
            return 'Attribute "position" must be "on" or "off".'

        return content


    def send_bad_request(self, message):
        self.send_response(400, message)
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

start_server()
