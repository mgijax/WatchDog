from statistic import *
from abc import ABCMeta, abstractmethod
import commands
import re

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
		string = commands.getstatusoutput('uptime')
		m = re.search('(\d+\.\d+).*(\d+\.\d+).*(\d+\.\d+)', string[1])
		return [
			Statistic("", "Load", "1min", m.group(1)),
			Statistic("", "Load", "5min", m.group(2)),
			Statistic("", "Load", "15min", m.group(3))]

class LinuxUptime(Command):
	def runCommand(self):
		string = commands.getstatusoutput('uptime')
		m = re.search('(\d+) day[^\d]+(\d+:\d+)', string[1])
		return [Statistic("", "System", "Uptime", m.group(1) + ":" + m.group(2))]

class LinuxUsers(Command):
	def runCommand(self):
		string = commands.getstatusoutput('uptime')
		m = re.search('(\d+) users', string[1])
		return [Statistic("", "System", "Users", m.group(1))]

class LinuxMem(Command):
	def runCommand(self):
		try:
			string = commands.getstatusoutput("free | tail -2 | head -1 | awk '{ print $3\":\"$4; }'")
			columns = string[1].split(":")
			return [
				Statistic("", "Memory", "Used", columns[0]),
				Statistic("", "Memory", "Free", columns[1]),
				Statistic("", "Memory", "Total", int(columns[0]) + int(columns[1]))]
		except:
			return []
class LinuxSwap(Command):
	def runCommand(self):
		string = commands.getstatusoutput("free | tail -1 | awk '{ print $2\":\"$3\":\"$4; }'")
		columns = string[1].split(":")
		return [
			Statistic("", "Swap", "Used", columns[1]),
			Statistic("", "Swap", "Free", columns[2]),
			Statistic("", "Swap", "Total", columns[0])]
