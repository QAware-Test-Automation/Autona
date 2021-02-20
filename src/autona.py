# AUTONA - UI automation server (Python 3)
# Copyright (C) 2021 Marco Alvarado
# Visit http://qaware.org

from http.server import HTTPServer
import server



def Serve(
    host = '0.0.0.0',
    port = 80):

    print(f'Autona serving at {host}:{port}')
    service = HTTPServer((host, port), server.Service)
    service.serve_forever()



if __name__ == '__main__':
    Serve()