from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_type = self.headers['Content-Type']
        content_length = int(self.headers['Content-Length'])

        if content_type != 'application/json':
            self.send_bad_request()
            return

        content = json.loads(self.rfile.read(content_length))
        id = content['id']
        on = content['on']

        print('Switching switch', id, 'on' if on else 'off')

        self.send_response(201)
        self.end_headers()

    def send_bad_request(self):
        self.send_response(400)
        self.end_headers()



def run():
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


run()
