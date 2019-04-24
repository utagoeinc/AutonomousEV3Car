# coding:utf-8
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
from urllib.parse import urlparse
from threading import Thread
from queue import Queue

import numpy as np
import cv2

import serial
import json
import base64
import io
import math

from train import Model

class myHandler(BaseHTTPRequestHandler):
    queue = None

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        query_dict = dict(urllib.parse.parse_qsl(parsed_path.query))

        self.queue.put('GET', query_dict)

        self.send_response(200)


    def do_POST(self):
        data = json.loads(self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8'))

        self.queue.put('POST', data)

        self.send_response(200)


class http_request_queue(Queue):
    def __init__(self):
        super().__init__()
        self.number_of_available_posts = 1
        self.number_of_current_posts = 0

    def put(self, method, object):
        if method == 'POST':
            if not self.is_available(method):
                return False
            else:
                self.number_of_current_posts = self.number_of_current_posts + 1

        item = {'method': method, 'object': object}
        super().put(item)
        return True

    def get(self):
        item = super().get()
        return item['method'], item['object']

    def is_available(self, method):
        if method == 'POST' and self.number_of_current_posts > 0:
            return False

        return True

    def set_available(self, available=True):
        if available:
            self.number_of_current_posts = 0
        else:
            self.number_of_current_posts = 1


class http_server:
    def __init__(self):
        port = 8080

        speed = 0.3 # 0.0 to 1.0
        self.quantized_speed = str(hex(math.ceil(abs(speed) * 15)))

        self.model = None
        self.bluetooth_port = serial.Serial('/dev/tty.MindstormsEV3-SerialPor', 115200)
        self.queue = http_request_queue()

        myHandler.queue = self.queue
        server = HTTPServer(('', port), myHandler)

        print("Starting Thread")
        exec_queue_thread = Thread(target=self.exec_queue, name='exec_queue_thread', args=())
        exec_queue_thread.start()

        print("Listening:", port)
        server.serve_forever()


    def exec_queue(self):
        self.model = Model(step=15000)

        while True:
            if not self.queue.empty():
                method, object = self.queue.get()

                if method == 'GET':
                    self.do_GET(object)
                else:
                    self.do_POST(object)
                    self.queue.set_available()


    def do_GET(self, query_dict):

        target = query_dict.get('target')
        amount = float(query_dict.get('amount'))

        return


    def do_POST(self, data):
        """ Control EV3 using an image send from iPhone """

        raw_image = base64.b64decode(data['image'])

        img_bin = io.BytesIO(raw_image)
        file_bytes = np.asarray(bytearray(img_bin.read()), dtype=np.uint8)
        image = np.array([cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)])
        action = self.model.predict(image)

        # Control EV3 with action
        if action == 0:
            self.bluetooth_port.write(b'j')
            self.bluetooth_port.write(b'f')
            print('LEFT')

            self.bluetooth_port.write(b'i')
            self.bluetooth_port.write(self.quantized_speed[-1:].encode())
            print('forward')
        elif action == 1:
            self.bluetooth_port.write(b'j')
            self.bluetooth_port.write(b'7')
            print('left')

            self.bluetooth_port.write(b'i')
            self.bluetooth_port.write(self.quantized_speed[-1:].encode())
            print('forward')
        elif action == 2:
            self.bluetooth_port.write(b'j')
            self.bluetooth_port.write(b'0')
            print('center')

            self.bluetooth_port.write(b'i')
            self.bluetooth_port.write(self.quantized_speed[-1:].encode())
            print('forward')
        elif action == 3:
            self.bluetooth_port.write(b'l')
            self.bluetooth_port.write(b'7')
            print('right')

            self.bluetooth_port.write(b'i')
            self.bluetooth_port.write(self.quantized_speed[-1:].encode())
            print('forward')
        elif action == 4:
            self.bluetooth_port.write(b'l')
            self.bluetooth_port.write(b'f')
            print('RIGHT')

            self.bluetooth_port.write(b'i')
            self.bluetooth_port.write(self.quantized_speed[-1:].encode())
            print('forward')
        else:
            self.bluetooth_port.write(b'i')
            self.bluetooth_port.write(b'0')
            print('stop')

        return


class main:
    def __init__(self):
        self.server = http_server()

if __name__ == '__main__':
    m = main()
