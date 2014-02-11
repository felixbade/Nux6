#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

class MessageLogger:

	def __init__(self, file):
		self.file = file

	def log(self, message):
		timestamp = time.strftime("%F %T")
		self.file.write('%s %s\n' % (timestamp, message))
		self.file.flush()

	def close(self):
		self.file.close()