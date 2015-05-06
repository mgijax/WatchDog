from datapoint import *
from abc import ABCMeta, abstractmethod
import commands
import time
import re

class Command:
	__metaclass__ = ABCMeta
	lastRuntime = 0

	def __init__(self, arch, freq):
		self.arch = arch
		try:
			self.freq = int(freq)
		except:
			self.freq = 60

	def runCommand(self):
		timeToRun = self.lastRuntime <= (time.time() - self.freq)
		if timeToRun:
			self.lastRuntime = time.time()
			return self.run()
		else:
			return []

	@abstractmethod
	def run(self):
		raise NotImplementedError()

# Produces a number that is Meg / Second
class DiskSpeed(Command):

	def __init__(self, arch, freq, volume):
		Command.__init__(self, arch, freq)
		self.volume = volume

	def run(self):
		start = time.time()
		string = commands.getstatusoutput("dd bs=10240 count=10240 if=/dev/zero of=" + self.volume)
		string = commands.getstatusoutput("dd bs=10240 count=10240 if=/dev/zero of=" + self.volume)
		string = commands.getstatusoutput("dd bs=10240 count=10240 if=/dev/zero of=" + self.volume)
		end = time.time()
		return [DataPoint("DiskSpeed", self.volume, str(int(300 / (end - start))))]

class DiskSize(Command):

	def __init__(self, arch, freq, volume):
		Command.__init__(self, arch, freq)
		self.volume = volume

	def run(self):
		string = commands.getstatusoutput("df -Ph " + self.volume + " | tail -1 | awk '{print $1\"->\"$6}'")
		string2 = commands.getstatusoutput("df -Ph " + self.volume + " | tail -1 | awk '{print $2\":\"$3\":\"$4}'")
		columns = string2[1].split(":")
		return [
			DataPoint("DiskUsed", string[1], columns[1]),
			DataPoint("DiskAvailable", self.volume, columns[2]),
			DataPoint("DiskTotal", self.volume, columns[0])]

class NetworkErrors(Command):

	def __init__(self, arch, freq, interface):
		Command.__init__(self, arch, freq)
		self.interface = interface

	def run(self):
		return [DataPoint("NetworkErrors", self.interface, "Value")]

class NetworkDrops(Command):

	def __init__(self, arch, freq, interface):
		Command.__init__(self, arch, freq)
		self.interface = interface

	def run(self):
		return [DataPoint("NetworkDrops", self.interface, "Value")]

class NetworkBandwidth(Command):

	def __init__(self, arch, freq, interface):
		Command.__init__(self, arch, freq)
		self.interface = interface

	def run(self):
		return [DataPoint("NetworkBandwidth", self.interface, "Value")]

class Load(Command):

	def __init__(self, arch, freq):
		Command.__init__(self, arch, freq)

	def run(self):
		string = commands.getstatusoutput("uptime")
		m = re.search('(\d+\.\d+).*(\d+\.\d+).*(\d+\.\d+)', string[1])
		return [
			DataPoint("SystemLoad", "1min", m.group(1)),
			DataPoint("SystemLoad", "5min", m.group(2)),
			DataPoint("SystemLoad", "15min", m.group(3))]

class Uptime(Command):

	def __init__(self, arch, freq):
		Command.__init__(self, arch, freq)

	def run(self):
		string = commands.getstatusoutput("uptime")
		m = re.search('(\d+) day[^\d]+(\d+:\d+)', string[1])
		return [DataPoint("System", "Uptime", m.group(1) + ":" + m.group(2))]

class Users(Command):

	def __init__(self, arch, freq):
		Command.__init__(self, arch, freq)

	def run(self):
		string = commands.getstatusoutput("uptime")
		m = re.search('(\d+) user', string[1])
		return [DataPoint("System", "Users", m.group(1))]

class MemoryRam(Command):

	def __init__(self, arch, freq):
		Command.__init__(self, arch, freq)

	def run(self):
		try:
			string = commands.getstatusoutput("free | tail -2 | head -1 | awk '{ print $3\":\"$4; }'")
			columns = string[1].split(":")
			return [
				DataPoint("MemoryRam", "Used", columns[0]),
				DataPoint("MemoryRam", "Free", columns[1]),
				DataPoint("MemoryRam", "Total", int(columns[0]) + int(columns[1]))]
		except:
			return []

class MemorySwap(Command):

	def __init__(self, arch, freq):
		Command.__init__(self, arch, freq)

	def run(self):
		try:
			string = commands.getstatusoutput("free | tail -1 | awk '{ print $2\":\"$3\":\"$4; }'")
			columns = string[1].split(":")
			return [
				DataPoint("MemroySwap", "Used", columns[1]),
				DataPoint("MemorySwap", "Free", columns[2]),
				DataPoint("MemorySwap", "Total", int(columns[1]) + int(columns[2]))]
		except:
			return []
