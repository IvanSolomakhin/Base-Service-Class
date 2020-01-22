"""
Example of using base Service class.
To run: python3 example.py 
"""

from time import sleep

import log
from log import Log
from service import Service, Package


class User(Service):
	"""
	User service.
	"""

	def __init__(self):
		super().__init__(self.__class__.__name__)


	def start(self):
		super().start()


	def askPlusOperation(self, a, b):
		Log.debug(str(a) + ", " + str(b))

		self.sendRequest(Package("Calculator", "plusOperation", [a, b], "User", "onPlusOperationDone"))


	def onPlusOperationDone(self, a, b, result):
		Log.debug(str(a) + " + " + str(b) + " = " + str(result))


class Calculator(Service):
	"""
	Calculator service.
	"""

	def __init__(self):
		super().__init__(self.__class__.__name__)


	def start(self):
		super().start()


	def plusOperation(self, a, b):
		Log.debug(str(a) + ", " + str(b))

		return a, b, a + b


def main():
	log.init("debug", "main.log")

	c = Calculator()
	u = User()

	c.start()
	u.start()

	sleep(1)

	u.askPlusOperation(34, 21)

	sleep(1)

	c.stop()
	u.stop()


if __name__ == '__main__':
	main()