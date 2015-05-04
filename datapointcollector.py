from abc import ABCMeta, abstractmethod

class DataPointCollector:
	__metaclass__ = ABCMeta

	@abstractmethod
	def runCommands(self):
		raise NotImplementedError()
