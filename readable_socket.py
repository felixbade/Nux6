#/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

class ReadableSocket(socket):

	def readBit(self):
		return self.makefile().readline()