"""
Module for recording logs. Different logging levels are available. 
To setup Log object call the init function.
"""

import logging
from logging.handlers import RotatingFileHandler


Log = logging.getLogger('root')

def init(logLevel, logName):
	"""
	docstring
	"""

	global Log

	level = logging.INFO

	if logLevel == 'debug':
		level = logging.DEBUG
	elif logLevel == 'warning':
		level = logging.WARNING
	elif logLevel == 'error':
		level = logging.ERROR

	formatter = logging.Formatter(fmt='[%(levelname)s, %(asctime)s] %(funcName)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S')
	fileHandler = logging.handlers.RotatingFileHandler(filename=logName, maxBytes=4000, backupCount=1)
	consoleHandler = logging.StreamHandler()

	fileHandler.setFormatter(formatter)
	consoleHandler.setFormatter(formatter)

	Log.setLevel(level)
	Log.addHandler(fileHandler)
	Log.addHandler(consoleHandler)
