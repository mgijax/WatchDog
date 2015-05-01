from abc import ABCMeta, abstractmethod

class Command:
	__metaclass__ = ABCMeta

	@abstractmethod
	def runCommand(self):
		raise NotImplementedError()

class LinuxMemoryCacheCommand(Command):
	def runCommand(self):
		return ["Cache", "Value"]

