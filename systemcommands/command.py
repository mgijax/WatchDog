from datapoint import *
import commands
import time

class Command:
	lastRuntime = 0

	def __init__(self, arch, freq):
		self.arch = arch
		try:
			self.freq = int(freq)
		except:
			self.freq = 60

	def setDebug(self, debug):
		self.debug = debug

	def runCommand(self):
		timeToRun = self.lastRuntime <= (time.time() - self.freq)
		if timeToRun:
			self.lastRuntime = time.time()
			try:
				if self.debug: print "Running " + self.__class__.__name__ + " Command"
				ret = self.run()
				if self.debug: print "Finished running " + self.__class__.__name__ + " Command"
				if self.debug: print
				return ret
			except Exception, e:
				if self.debug: print "Error: " + str(e)
				if self.debug: print "Finished running " + self.__class__.__name__ + " Command"
				if self.debug: print
				return []
		else:
			if self.debug: print self.__class__.__name__ + " is sleeping for " + str(int(self.freq - (time.time() - self.lastRuntime))) + " more seconds"
			return []

	def run(self):
		raise NotImplementedError()

