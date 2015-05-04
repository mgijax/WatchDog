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
		if(type == "system"):
			self.setupSystem(self.config['system_types'].split(','))
		elif(type == "memory"):
			self.setupMemory(self.config['memory_types'].split(','))
		elif(type == "disk"):
			self.setupDisk(self.config['disk_types'].split(','))
		elif(type == "network"):
			self.setupNetwork(self.config['network_types'].split(','))
		else:
			print "Unknown Collection Type: %s" % type

	def setupSystem(self, loadTypes):
		for loadType in loadTypes:
			if(loadType == "system_load"):
				self.list.append(LinuxLoad(self.config['system_load_freq']))
			elif(loadType == "system_uptime"):
				self.list.append(LinuxUptime(self.config['system_uptime_freq']))
			elif(loadType == "system_users"):
				self.list.append(LinuxUsers(self.config['system_users_freq']))

	def setupMemory(self, memoryTypes):
		for memoryType in memoryTypes:
			if(memoryType == "mem"):
				self.list.append(LinuxMem(self.config['mem_freq']))
			elif(memoryType == "swap"):
				self.list.append(LinuxSwap(self.config['swap_freq']))

	def setupDisk(self, disk_types):
		for diskType in disk_types:
			if(diskType == "disk_speed"):
				for volume in self.config['disk_volumes'].split(','):
					self.list.append(LinuxDiskSpeed(volume, self.config['disk_speed_freq']))
			elif(diskType == "disk_size"):
				for volume in self.config['disk_volumes'].split(','):
					self.list.append(LinuxDiskSize(volume, self.config['disk_size_freq']))

	def setupNetwork(self, network_types):
		for networkType in network_types:
			if(networkType == "network_errors"):
				for interface in self.config['network_interfaces'].split(','):
					self.list.append(LinuxNetworkErrors(interface, self.config['network_errors_freq']))
			elif(networkType == "network_drops"):
				for interface in self.config['network_interfaces'].split(','):
					self.list.append(LinuxNetworkDrops(interface, self.config['network_drops_freq']))
			elif(networkType == "network_bandwidth"):
				for interface in self.config['network_interfaces'].split(','):
					self.list.append(LinuxNetworkBandwidth(interface, self.config['network_bandwidth_freq']))

	def runCommands(self):
		dataPointObjects = []
		for command in self.list:
			dataPointObjects.extend(command.runCommand())
		for dp in dataPointObjects:
			dp.server_name = self.serverName
		return dataPointObjects
