from abc import ABCMeta, abstractmethod

class StatsCollector:
	__metaclass__ = ABCMeta

	@abstractmethod
	def runCommands(self):
		raise NotImplementedError()
