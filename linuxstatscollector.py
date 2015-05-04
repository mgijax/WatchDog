from linuxcommands import *
from statscollector import StatsCollector

class LinuxStatsCollector(StatsCollector):

	def __init__(self, config):
		self.list = []
		self.serverName = config['server_name']
		self.arch = config['server_arch']
		self.config = config
		self.setupTypes(self.config['collection_types'].split(','))

	def setupTypes(self, typeList):
		for type in typeList:
			self.setupType(type)

	def setupType(self, type):
		if(type == "load"):
			self.setupLoad(self.config['load_types'].split(','))
		elif(type == "memory"):
			self.setupMemory(self.config['memory_types'].split(','))
		elif(type == "disk"):
			self.setupDisk(self.config['disk_types'].split(','))
		elif(type == "network"):
			self.setupNetwork(self.config['network_types'].split(','))
		else:
			print "Unknown Collection Type: %s" % type

	def setupLoad(self, loadTypes):
		for loadType in loadTypes:
			if(loadType == "load"):
				self.list.append(LinuxLoad())
			elif(loadType == "uptime"):
				self.list.append(LinuxUptime())
			elif(loadType == "users"):
				self.list.append(LinuxUsers())

	def setupMemory(self, memoryTypes):
		for memoryType in memoryTypes:
			if(memoryType == "mem"):
				self.list.append(LinuxMem())
			elif(memoryType == "swap"):
				self.list.append(LinuxSwap())

	def setupDisk(self, disk_types):
		for diskType in disk_types:
			if(diskType == "speed"):
				for volume in self.config['disk_volumes'].split(','):
					self.list.append(LinuxDiskSpeed(volume))
			elif(diskType == "size"):
				for volume in self.config['disk_volumes'].split(','):
					self.list.append(LinuxDiskSize(volume))

	def setupNetwork(self, network_types):
		for networkType in network_types:
			if(networkType == "errors"):
				for interface in self.config['network_interfaces'].split(','):
					self.list.append(LinuxNetworkErrors(interface))
			elif(networkType == "bandwidth"):
				for interface in self.config['network_interfaces'].split(','):
					self.list.append(LinuxNetworkBandwidth(interface))

	def runCommands(self):
		statObjects = []
		for command in self.list:
			statObjects.extend(command.runCommand())
		for stat in statObjects:
			stat.server_name = self.serverName
		print statObjects
