from statistic import *
from abc import ABCMeta, abstractmethod

class Command:
	__metaclass__ = ABCMeta

	@abstractmethod
	def runCommand(self):
		raise NotImplementedError()

class LinuxDiskSpeed(Command):
	def __init__(self, volume):
		self.volume = volume
	def runCommand(self):
		return [Statistic("", "DiskSpeed", self.volume, "Value")]

class LinuxDiskSize(Command):
	def __init__(self, volume):
		self.volume = volume
	def runCommand(self):
		return [Statistic("", "DiskSize", self.volume, "Value")]

class LinuxNetwork(Command):
	def __init__(self, network):
		self.network = network
	def runCommand(self):
		return [Statistic("", "Network", self.network, "Value")]

class LinuxLoad(Command):
	def runCommand(self):
		return [
			Statistic("", "Load", "1min", "Value"),
			Statistic("", "Load", "5min", "Value"),
			Statistic("", "Load", "15min", "Value")]

class LinuxUptime(Command):
	def runCommand(self):
		return [Statistic("", "System", "Uptime", "Value")]

class LinuxUsers(Command):
	def runCommand(self):
		return [Statistic("", "System", "Users", "Value")]

class LinuxMem(Command):
	def runCommand(self):
		return [
			Statistic("", "Memory", "Used", "Value"),
			Statistic("", "Memory", "Free", "Value"),
			Statistic("", "Memory", "Total", "Value")]

class LinuxSwap(Command):
	def runCommand(self):
		return [
			Statistic("", "Swap", "Used", "Value"),
			Statistic("", "Swap", "Free", "Value"),
			Statistic("", "Swap", "Total", "Value")]
