#/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
from threading import Thread
from select import select

DEFAULT_RECONNECT_TIMEOUT = 300

#TODO: output
#TODO: check variable name spelling
#TODO: re-order functions

class ReconnectingSocket(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.setUpTCPSocketForIPv4()
        self.reconnect_timeout = DEFAULT_RECONNECT_TIMEOUT

    def setUpTCPSocketForIPv4(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketfile = socket.makefile()
    
    def setRemoteAddress(self, address):
        self.address = address

    def setReconnectTimeout(self, seconds):
        self.reconnect_timeout = seconds

    def setInputHandlerFunction(self, function):
        self.input_handler_function = function

    def run(self):
        while True:
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

    def receiveData(self):
        self.received_data = self.socketfile.readiline()
    
    def handleReceivedData(self):
        #TODO: handler function is not set
        self.input_handler_function(self.received_data)
