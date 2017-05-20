#!/usr/bin/env python3

import json
import signal
import socket
import sys
import threading
import time

import lightServerBackend

num_LEDs = 160
ip_addr = "127.0.0.1"

class LightServer(object):
    def __init__(self):
        self._socket = socket.socket()
        self._n_requests = None

        self.msg_type = None
        self.brightness = 31
        self.pattern = "solid"
        self.pattern_time = -1
        self.hz = -1
        self.color = "ffffff"
        self.reply = None
        self.thread = lightServerBackend.server(
                           thread_ID = 1,
                           effect = "strandTest")


    def define_socket(self, port, n_requests=5):
        """
            Used to define the socket object from inputs
        """
        host = socket.gethostname()
        print("Hostname is %s" % str(host))
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind((ip_addr, port))
        self._n_requests = n_requests


    def handle_requests(self):
        self._socket.listen(self._n_requests)

        while True:
            client, address = self._socket.accept()
            print("Connected to %s" % str(address))

            try:
                json_data = str(client.recv(1024).decode("utf8"))
                data = json.loads(json_data)
                self.msg_type = data['msgType']
                if self.msg_type == "set":
                    self.pattern = data['pattern']
                    self.pattern_time = data['patternTime']
                    self.brightness = data['brightness']
                    self.color = data['color']
                    self.hz = data['hz']
                    print(data)
                elif self.msg_type == "start":
                    print("Starting lights")
                    if(self.thread.is_alive()):
                        self.thread.terminate(False)
                    self.thread = lightServerBackend.server(
                                       brightness = int(self.brightness),
                                       effect = self.pattern,
                                       pause_time = (1/int(self.hz)),
                                       run_time = self.pattern_time,
                                       strip_color = self.color,
                                       thread_ID = 1,
                                       num_LEDs = num_LEDs)
                    self.thread.start()
                elif self.msg_type == "stop":
                    print("Stopping lights")
                    if(self.thread.is_alive()):
                        self.thread.terminate()
            except KeyError:
                client.send("Invalid JSON Passed")
                print("Invalid JSON Passed")
                client.close()
                return

            # Try sending the reply line-by line because of the text cut-off
            self.reply = 'Hello this is a test'

            for line in self.reply.split('\n'):
                client.send(bytes(line+'\n', 'UTF-8'))

            print("Sent Reply, Closing Connection")
            client.close()

    def terminate(self):
        if(self.thread.is_alive()):
            self.thread.terminate()


def exit_gracefully(signum, frame):
   signal.signal(signal.SIGINT, original_sigint)

   try:
      print("\nTrying to do some cleanup before exiting...")
      server.terminate()
   finally:
      sys.exit(1)

   # restore the exit gracefully handler
   signal.signal(signal.SIGINT, exit_gracefully)


if __name__ == '__main__':
    # store the original SIGINT handler
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)

    # start the LightServer
    server = LightServer()
    server.define_socket(915, 5)
    server.handle_requests()
