# AUTONA - UI automation server (Python 3)
# Copyright (C) 2021 Marco Alvarado
# Visit http://qaware.org

from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import html
import base64

import time

import os
import platform

from utils import Integer
from language_en import language

historyFile = 'history.txt'



# Do you require a multi-threading or SSL server? Contact us at autona@qaware.org
class Service(
    BaseHTTPRequestHandler):

    automator = None    # : Automator



    def Receive(
        self,
        paths,
        parameters):

        print(paths)
        print(parameters)

        page = ''

        if paths == ['']:  # root path
            history = ''
            result = ''

            if 'commands' in parameters:
                commands = parameters['commands'][0]

                # Run commands.
                start = 0
                end = len(commands)
                if 'start' in parameters: start = int(parameters['start'][0])
                if 'end'   in parameters: end   = int(parameters['end'][0])
                result = self.RunCommands(commands, start, end)

                # Add commands to history.
                if os.path.exists(historyFile):
                    history = open(historyFile, 'r', encoding = 'utf-8').read()
                history = commands.replace('\r', '') + '\n' + history
                open(historyFile, 'w', encoding = 'utf-8').write(history)

            # Capture the screen.
            screen = Service.automator.CaptureScreen()
            screen = 'data:image/png;base64,' + str(base64.b64encode(screen).decode('utf-8'))
            (screenWidth, screenHeight) = Service.automator.ScreenSize()

            # Generate HTML.
            page = open('web/index.html', encoding = 'utf-8').read()
            page = page.replace('{title}', html.escape(platform.platform(), 1))
            page = page.replace('{commands}', html.escape(commands, 1))
            page = page.replace('{history}', html.escape(history, 1))
            page = page.replace('{result}', html.escape(result, 1))
            page = page.replace('{screen}', screen, 1)
            page = page.replace('{screenWidth}', str(screenWidth), 1)
            page = page.replace('{screenHeight}', str(screenHeight), 1)

        # Send response.
        self.RespondHeaders()
        self.wfile.write(page.encode('utf-8'))



    # For improved command interpreter contact us at autona@qaware.org
    def RunCommands(
        self,
        commands,
        start, end):

        result = ''
        i = Integer(start)
        delay = 0.2

        while i.value < end:
            if Compare(commands, '{', i):
                if Compare(commands, '{}', i):
                    if delay > 0: time.sleep(delay)
                    Service.automator.TapKeys('{')

                elif Compare(commands, '}}', i):
                    if delay > 0: time.sleep(delay)
                    Service.automator.TapKeys('}')

                elif Compare(commands, language['slow'], i):
                    delay = 0.2
                    if not Compare(commands, '}', i):
                        delay = float(GetValue(commands, i))
                        Compare(commands, '}', i)

                elif Compare(commands, language['fast'], i):
                    delay = 0
                    Compare(commands, '}', i)

                elif Compare(commands, language['wait'], i):
                    seconds = 5
                    if not Compare(commands, '}', i):
                        delay = float(GetValue(commands, i))
                        Compare(commands, '}', i)
                    time.sleep(seconds)

                elif Compare(commands, language['move'], i):
                    x = float(GetValue(commands, i))
                    y = float(GetValue(commands, i))
                    Compare(commands, '}', i)
                    Service.automator.MovePointer(x, y, delay > 0)

                elif Compare(commands, language['press'], i):
                    Compare(commands, '}', i)

                elif Compare(commands, language['release'], i):
                    Compare(commands, '}', i)

                elif Compare(commands, language['open'], i):
                    file = GetValue(commands, i)
                    Compare(commands, '}', i)
                    os.startfile(file)

                elif Compare(commands, language['system'], i):
                    Compare(commands, '}', i)
                    (screenWidth, screenHeight) = Service.automator.ScreenSize()
                    result += \
                        'system: ' + platform.platform() + '\n' \
                        'screen: ' + str(screenWidth) + ' ' + str(screenHeight) + '\n'

                elif Compare(commands, language['clear'], i):
                    Compare(commands, '}', i)
                    open(historyFile, 'w+', encoding = 'utf-8').write('')

        return result



    def RespondHeaders(
        self,
        responseCode = 200,         # https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
        contentType = 'text/html'): # https://www.iana.org/assignments/media-types/media-types.xhtml

        self.send_response(responseCode)
        self.send_header('content-type', contentType)
        self.end_headers()



    def ParsePaths(
        self):

        paths = urlparse(self.path).path.split('/')
        paths.pop(0)
        return paths



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

        paths = self.ParsePaths()
        parameters = self.ParseQuery()
        self.Receive(paths, parameters)



    def do_POST(
        self):

        # Sample POST request:
        # curl -d "c=d" http://localhost?a=b

        paths = self.ParsePaths()
        parameters = self.ParseQuery()
        parameters.update(self.ParseContent())
        self.Receive(paths, parameters)



    def do_HEAD(
        self):

        # Sample HEAD request: 
        # curl -I http://localhost

        self.RespondHeaders()



def Compare(
    string,
    substring,
    position):  # : Integer

    i = position.value
    l = len(substring)
    p = string.find(substring, i, i + l)
    if p == i:
        position += l
        return True



def GetValue(
    string,
    position):  # : Integer

    # Skip first spaces.
    i0 = position.value
    l = len(string)
    while i0 < l and string[i0] == ' ':
        i0 += 1

    # Walk through string until finding spaces.
    i1 = i0
    while i1 < l and not string[i1] in [' ', '}']:
        i1 += 1

    s = string[i0:i1]
    position.value = i1
    return s