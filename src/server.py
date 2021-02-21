# AUTONA - UI automation server (Python 3)
# Copyright (C) 2021 Marco Alvarado
# Visit http://qaware.org

from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import base64

import platform

automator = None



class Service(
    BaseHTTPRequestHandler):

    def Receive(
        self,
        parameters):

        print(parameters)

        # Capture the screen.
        screen = automator.CaptureScreen()
        screen = 'data:image/png;base64,' + str(base64.b64encode(screen).decode('utf-8'))
        (screenWidth, screenHeight) = automator.ScreenSize()

        # Generate HTML.
        html = open('web/index.html', encoding = 'utf-8').read()
        html = html.replace('{title}', platform.platform(), 1)
        html = html.replace('{screen}', screen, 1)
        html = html.replace('{screenWidth}', str(screenWidth), 1)
        html = html.replace('{screenHeight}', str(screenHeight), 1)

        # Send response.
        self.RespondHeaders()
        self.wfile.write(html.encode('utf-8'))



    def RespondHeaders(
        self,
        responseCode = 200,         # https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
        contentType = 'text/html'): # https://www.iana.org/assignments/media-types/media-types.xhtml

        self.send_response(responseCode)
        self.send_header('content-type', contentType)
        self.end_headers()



    def ParseQuery(
        self):

        parameters = parse_qs(urlparse(self.path).query)
        return parameters



    def ParseContent(
        self):

        contentLength = int(self.headers['content-length'])
        content = self.rfile.read(contentLength).decode('utf-8')
        parameters = parse_qs(content)
        return parameters



    def do_GET(
        self):

        # Sample GET request: 
        # curl http://localhost?a=b

        parameters = self.ParseQuery()
        self.Receive(parameters)



    def do_POST(
        self):

        # Sample POST request:
        # curl -d "c=d" http://localhost?a=b

        parameters = self.ParseQuery()
        parameters.update(self.ParseContent())
        self.Receive(parameters)



    def do_HEAD(
        self):

        # Sample HEAD request: 
        # curl -I http://localhost

        self.RespondHeaders()