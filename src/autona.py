# AUTONA - UI automation server (Python 3)
# Copyright (C) 2021 Marco Alvarado
# Visit http://qaware.org

from automator_autopy import AutomatorAutoPy

from http.server import HTTPServer
from server import Service



def Serve(
    automatorClass,
    host = '0.0.0.0',
    port = 80):

    print(f'Autona serving at {host}:{port}')
    Service.automator = automatorClass()
    server = HTTPServer((host, port), Service)
    server.serve_forever()



if __name__ == '__main__':
    Serve(AutomatorAutoPy)