"""
Unit tests for service module.
To run: python3 -m unittest -v test
"""

import unittest
from time import sleep

from service import Service, Package


class TestService(unittest.TestCase):
	"""
	Class provides tests for Service base class.
	"""

	# TestService._workerTimeout - service worker timeout.
	_workerTimeout = 0
	# TestService._numWorkerThreads - count of service worker threads.
	_numWorkerThreads = 10 
	# TestService._jobQueueMaxSize - service job queue max size.
	_jobQueueMaxSize = 10000

	class Sender(Service):
		"""
		Test class Sender service.
		"""

		def __init__(self):
			super().__init__(self.__class__.__name__, TestService._workerTimeout, 
				TestService._numWorkerThreads,	TestService._jobQueueMaxSize)

			self.result = 0
			self.jobs = []


		def start(self):
			super().start()


		def sendNoneWithoutResponse(self):
			self.sendRequest(Package("Receiver", "receiveNone"))	


		def sendNone(self):
			self.sendRequest(Package("Receiver", "receiveNone", None, "Sender", "onReceiveNoneDone"))


		def sendNumber(self, a):
			self.sendRequest(Package("Receiver", "receiveNumber", a, "Sender", "onReceiveNumberDone"))


		def sendPair(self, a, b):
			self.sendRequest(Package("Receiver", "receivePair", [a, b], "Sender", "onReceivePairDone"))			


		def sendTuple(self, a, b, c):
			self.sendRequest(Package("Receiver", "receiveTuple", (a, b, c), "Sender", "onReceiveTupleDone"))


		def sendJob(self, a):
			self.sendRequest(Package("Receiver", "receiveNumber", a, "Sender", "onReceiveJobDone"))


		def onReceiveNoneDone(self):
			self.result = None


		def onReceiveNumberDone(self, a):
			self.result = a


		def onReceivePairDone(self, a, b):
			self.result = a, b


		def onReceiveTupleDone(self, a, b, c):
			self.result = a, b, c


		def onReceiveJobDone(self, a):
			self.jobs.append(a)


	class Receiver(Service):
		"""
		Test class Receiver service.
		"""

		def __init__(self):
			super().__init__(self.__class__.__name__, TestService._workerTimeout, 
				TestService._numWorkerThreads,	TestService._jobQueueMaxSize)

			self.receive = False

		def start(self):
			super().start()


		def receiveNone(self):
			self.receive = True


		def receiveNumber(self, a):
			self.receive = True
			return a


		def receivePair(self, a, b):
			self.receive = True
			return a, b


		def receiveTuple(self, a, b, c):
			self.receive = True
			return a, b, c


	def testStartStop(self):
		"""
		Tests start and stop methods.
		"""

		u = TestService.Sender()
		c = TestService.Receiver()

		u.start()
		c.start()

		self.assertTrue(u.state())
		self.assertTrue(u.state())

		u.stop()
		c.stop()

		self.assertFalse(c.receive)
		self.assertFalse(u.state())
		self.assertFalse(u.state())


	def testSendNone(self):
		"""
		Tests send request and responce methods with None argument.
		"""

		u = TestService.Sender()
		c = TestService.Receiver()

		u.start()
		c.start()

		sleep(1)
		u.sendNone()
		sleep(1)

		self.assertTrue(c.receive)
		self.assertEqual(u.result, None)

		u.stop()
		c.stop()


	def testSendNoneWithoutResponse(self):
		"""
		Tests send request and responce methods with without arguments.
		"""

		u = TestService.Sender()
		c = TestService.Receiver()

		u.start()
		c.start()

		sleep(1)
		u.sendNoneWithoutResponse()
		sleep(1)

		u.stop()
		c.stop()

		self.assertTrue(c.receive)
		self.assertFalse(u.state())
		self.assertFalse(u.state())

	def testSendNumber(self):
		"""
		Tests send request and responce methods with one argument.
		"""

		u = TestService.Sender()
		c = TestService.Receiver()

		u.start()
		c.start()

		a = 1

		sleep(1)
		u.sendNumber(a)
		sleep(1)

		self.assertTrue(c.receive)
		self.assertEqual(u.result, a)

		u.stop()
		c.stop()


	def testSendPair(self):
		"""
		Tests send request and responce methods with pair of arguments.
		"""

		u = TestService.Sender()
		c = TestService.Receiver()

		u.start()
		c.start()

		a = 121
		b = 221

		sleep(1)
		u.sendPair(a, b)
		sleep(1)

		self.assertTrue(c.receive)
		self.assertEqual(u.result, (a, b))

		u.stop()
		c.stop()


	def testSendTuple(self):
		"""
		Tests send request and responce methods with tuple argument.
		"""

		u = TestService.Sender()
		c = TestService.Receiver()

		u.start()
		c.start()

		a = 12
		b = 21
		e = 342

		sleep(1)
		u.sendTuple(a, b, e)
		sleep(1)

		self.assertTrue(c.receive)
		self.assertEqual(u.result, (a, b, e))

		u.stop()
		c.stop()


	def testSendJobs(self):
		"""
		Tests send request and responce methods with 10000 calls.
		"""

		u = TestService.Sender()
		c = TestService.Receiver()

		u.start()
		c.start()

		a = 1
		jobs = []

		sleep(1)

		i = 0
		while i != 10000:
			jobs.append(a)
			u.sendJob(a)
			a += 7
			i += 1

		sleep(1)

		self.assertTrue(c.receive)
		self.assertEqual(u.jobs.sort(), jobs.sort())

		u.stop()
		c.stop()


if __name__ == '__main__':
	unittest.main()
