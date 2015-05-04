from datapoint import *
from abc import ABCMeta, abstractmethod
import commands
import time
import re

class Command:
	__metaclass__ = ABCMeta
	lastRuntime = 0

	@abstractmethod
	def runCommand(self):
		raise NotImplementedError()

	def setFreq(self, freq):
		try:
			self.freq = int(freq)
		except:
			self.freq = 60

	def timeToRun(self):
		timeToRun = self.lastRuntime <= (time.time() - self.freq)
		if timeToRun:
			self.lastRuntime = time.time()
		return timeToRun


class LinuxDiskSpeed(Command):
	def __init__(self, volume, freq):
		self.volume = volume
		self.setFreq(freq)
	def runCommand(self):
		if self.timeToRun():
			return [DataPoint("", "DiskSpeed", self.volume, "Value")]
		else:
			return []

class LinuxDiskSize(Command):
	def __init__(self, volume, freq):
		self.volume = volume
		self.setFreq(freq)
	def runCommand(self):
		if self.timeToRun():
			return [DataPoint("", "DiskSize", self.volume, "Value")]
		else:
			return []

class LinuxNetworkErrors(Command):
	def __init__(self, interface, freq):
		self.interface = interface
		self.setFreq(freq)
	def runCommand(self):
		if self.timeToRun():
			return [DataPoint("", "NetworkErrors", self.interface, "Value")]
		else:
			return []

class LinuxNetworkBandwidth(Command):
	def __init__(self, interface, freq):
		self.interface = interface
		self.setFreq(freq)
	def runCommand(self):
		if self.timeToRun():
			return [DataPoint("", "NetworkBandwidth", self.interface, "Value")]
		else:
			return []

class LinuxLoad(Command):
	def __init__(self, freq):
		self.setFreq(freq)
	def runCommand(self):
		if self.timeToRun():
			string = commands.getstatusoutput('uptime')
			m = re.search('(\d+\.\d+).*(\d+\.\d+).*(\d+\.\d+)', string[1])
			return [
				DataPoint("", "Load", "1min", m.group(1)),
				DataPoint("", "Load", "5min", m.group(2)),
				DataPoint("", "Load", "15min", m.group(3))]
		else:
			return []

class LinuxUptime(Command):
	def __init__(self, freq):
		self.setFreq(freq)

	def runCommand(self):
		if self.timeToRun():
			string = commands.getstatusoutput('uptime')
			m = re.search('(\d+) day[^\d]+(\d+:\d+)', string[1])
			return [DataPoint("", "System", "Uptime", m.group(1) + ":" + m.group(2))]
		else:
			return []

class LinuxUsers(Command):
	def __init__(self, freq):
		self.setFreq(freq)

	def runCommand(self):
		if self.timeToRun():
			string = commands.getstatusoutput('uptime')
			m = re.search('(\d+) users', string[1])
			return [DataPoint("", "System", "Users", m.group(1))]
		else:
			return []

class LinuxMem(Command):
	def __init__(self, freq):
		self.setFreq(freq)

	def runCommand(self):
		if self.timeToRun():
			try:
				string = commands.getstatusoutput("free | tail -2 | head -1 | awk '{ print $3\":\"$4; }'")
				columns = string[1].split(":")
				return [
					DataPoint("", "Memory", "Used", columns[0]),
					DataPoint("", "Memory", "Free", columns[1]),
					DataPoint("", "Memory", "Total", int(columns[0]) + int(columns[1]))]
			except:
				return []
		else:
			return []

class LinuxSwap(Command):

	def __init__(self, freq):
		self.setFreq(freq)

	def runCommand(self):
		if self.timeToRun():
			try:
				string = commands.getstatusoutput("free | tail -1 | awk '{ print $2\":\"$3\":\"$4; }'")
				columns = string[1].split(":")
				return [
					DataPoint("", "Swap", "Used", columns[1]),
					DataPoint("", "Swap", "Free", columns[2]),
					DataPoint("", "Swap", "Total", int(columns[1]) + int(columns[2]))]
			except:
				return []
		else:
			return []
