#/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
from threading import Thread
from select import select

DEFAULT_RECONNECT_TIMEOUT = 300
DEFAULT_LOCAL_ADDRESS = ('', 0)

#TODO: check variable name spelling
#TODO: re-order functions

class ReconnectingSocket(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.reconnect_timeout = DEFAULT_RECONNECT_TIMEOUT
        self.local_address = DEFAULT_LOCAL_ADDRESS

    def run(self):
        self.connect()
        while True:
            self.receiveCycle()

    def receiveCycle(self):
        if self.didReceiveDataInTimeout():
            self.handleReceivedData()
        else:
            self.reconnect()

    def didReceiveDataInTimeout(self):
        if select([self.socket], [], [], self.reconnect_timeout)[0]:
            self.receiveData()
            return True
        else:
            return False

    def blockingSend(self, data):
        for line in data.split('\n'):
            self.socket.send(line + '\r\n')

    def reconnect(self):
        self.disconnect()
        self.connect()

    def connect(self):
        self.setUpTCPSocketForIPv4()
        self.socket.connect(self.address)

    def disconnect(self):
        self.socket.close()

    def setUpTCPSocketForIPv4(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(self.local_address)
        self.socketfile = socket.makefile()
    
    def receiveData(self):
        self.received_data = self.socketfile.readiline()
    
    def handleReceivedData(self):
        #TODO: handler function is not set
        self.input_handler_function(self.received_data)

    def setRemoteAddress(self, address):
        self.address = address

    def setLocalAddress(self, address):
        self.local_address = address

    def setReconnectTimeout(self, seconds):
        self.reconnect_timeout = seconds

    def setInputHandlerFunction(self, function):
        self.input_handler_function = function