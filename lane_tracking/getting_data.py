# coding:utf-8
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
from urllib.parse import urlparse
from threading import Thread
from queue import Queue

import serial
import json
import base64
import os
import datetime


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

        self.bluetooth_port = serial.Serial('/dev/tty.MindstormsEV3-SerialPor', 115200)
        self.queue = http_request_queue()

        self.current_action = 2
        self.image_index = 0
        self.skipping = True

        now = datetime.datetime.now()
        self.exec_datetime = now.strftime('%Y-%m-%d_%H-%M-%S')
        os.makedirs(os.path.join(os.getcwd(), 'data', self.exec_datetime, 'images'), exist_ok=True)
        self.save_dir = os.path.join(os.getcwd(), 'data', self.exec_datetime)
        self.action_txt = os.path.join(os.getcwd(), 'data', self.exec_datetime, 'actions.txt')

        self.prev_time = datetime.datetime.now()

        myHandler.queue = self.queue
        server = HTTPServer(('', port), myHandler)

        print("Starting Thread")
        exec_queue_thread = Thread(target=self.exec_queue, name='exec_queue_thread', args=())
        exec_queue_thread.start()

        print("Listening:", port)
        server.serve_forever()


    def exec_queue(self):
        while True:
            if not self.queue.empty():
                method, object = self.queue.get()

                if method == 'GET':
                    self.do_GET(object)
                else:
                    self.do_POST(object)
                    self.queue.set_available()


    def do_GET(self, query_dict):
        if (datetime.datetime.now() - self.prev_time).seconds > 0:
            self.prev_time = datetime.datetime.now()

            target = query_dict.get('target')
            amount = float(query_dict.get('amount'))

            if target == 'front':
                if amount == 1.0:
                    self.current_action = 4
                elif amount == 0.5:
                    self.current_action = 3
                elif amount == -0.5:
                    self.current_action = 1
                elif amount == -1.0:
                    self.current_action = 0
                else:
                    self.current_action = 2

                self.control(self.current_action)
                self.skipping = True

            else:
                self.skipping = False

        return


    def do_POST(self, data):
        if not self.skipping:
            raw_image = base64.b64decode(data['image'])

            with open(os.path.join(self.save_dir, 'images', '{:04}.jpg'.format(self.image_index)), 'wb') as image_file:
                image_file.write(raw_image)
                self.image_index = self.image_index + 1

            with open(self.action_txt, 'a') as action_txt:
                action_txt.write('{}\n'.format(self.current_action))

        self.skipping = True
        return


    def control(self, action=2):
        if action == 0:
            self.bluetooth_port.write(b'j')
            self.bluetooth_port.write(b'f')
            print('LEFT')

        elif action == 1:
            self.bluetooth_port.write(b'j')
            self.bluetooth_port.write(b'7')
            print('left')

        elif action == 2:
            self.bluetooth_port.write(b'j')
            self.bluetooth_port.write(b'0')
            print('center')

        elif action == 3:
            self.bluetooth_port.write(b'l')
            self.bluetooth_port.write(b'7')
            print('right')

        elif action == 4:
            self.bluetooth_port.write(b'l')
            self.bluetooth_port.write(b'f')
            print('RIGHT')

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
