from linuxcommands import *
from datapointcollector import DataPointCollector

class LinuxDataPointCollector(DataPointCollector):

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
				self.list.append(LinuxLoad(self.config['load_freq']))
			elif(loadType == "uptime"):
				self.list.append(LinuxUptime(self.config['uptime_freq']))
			elif(loadType == "users"):
				self.list.append(LinuxUsers(self.config['users_freq']))

	def setupMemory(self, memoryTypes):
		for memoryType in memoryTypes:
			if(memoryType == "mem"):
				self.list.append(LinuxMem(self.config['mem_freq']))
			elif(memoryType == "swap"):
				self.list.append(LinuxSwap(self.config['swap_freq']))

	def setupDisk(self, disk_types):
		for diskType in disk_types:
			if(diskType == "speed"):
				for volume in self.config['disk_volumes'].split(','):
					self.list.append(LinuxDiskSpeed(volume, self.config['speed_freq']))
			elif(diskType == "size"):
				for volume in self.config['disk_volumes'].split(','):
					self.list.append(LinuxDiskSize(volume, self.config['size_freq']))

	def setupNetwork(self, network_types):
		for networkType in network_types:
			if(networkType == "errors"):
				for interface in self.config['network_interfaces'].split(','):
					self.list.append(LinuxNetworkErrors(interface, self.config['errors_freq']))
			elif(networkType == "bandwidth"):
				for interface in self.config['network_interfaces'].split(','):
					self.list.append(LinuxNetworkBandwidth(interface, self.config['bandwidth_freq']))

	def runCommands(self):
		dataPointObjects = []
		for command in self.list:
			dataPointObjects.extend(command.runCommand())
		for dp in dataPointObjects:
			dp.server_name = self.serverName
		return dataPointObjects
