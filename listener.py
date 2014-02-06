#/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Thread

class Listener(Thread):

    def __init__(self, readable_object):
        Thread.__init__(self)
        self.daemon = True
        self.readable_object = readable_object

    def run(self):
        while True:
            data = self.readable_object.readBit()
            self.input_handler_function(data)
        
    def setInputHandlerFunction(self, function):
        self.input_handler_function = function