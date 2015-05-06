from systemcommands import *

class DataPointCollector():

	def __init__(self, config):
		self.list = []
		self.serverName = config['server_name']
		self.arch = config['server_arch']
		self.config = config
		self.setupCollectionTypes(self.config['collection_types'].split(','))

	def setupCollectionTypes(self, typeList):
		for collectionType in typeList:
			self.setupType(collectionType)

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

	def setupSystem(self, systemTypes):
		for systemType in systemTypes:
			if(systemType == "system_load"):
				self.list.append(Load(self.arch, self.config['system_load_freq']))
			elif(systemType == "system_uptime"):
				self.list.append(Uptime(self.arch, self.config['system_uptime_freq']))
			elif(systemType == "system_users"):
				self.list.append(Users(self.arch, self.config['system_users_freq']))
			else:
				print "Unknown System Type: %s" % systemType

	def setupMemory(self, memoryTypes):
		for memoryType in memoryTypes:
			if(memoryType == "mem"):
				self.list.append(Mem(self.arch, self.config['mem_freq']))
			elif(memoryType == "swap"):
				self.list.append(Swap(self.arch, self.config['swap_freq']))

	def setupDisk(self, disk_types):
		for diskType in disk_types:
			if(diskType == "disk_speed"):
				for volume in self.config['disk_volumes'].split(','):
					self.list.append(DiskSpeed(self.arch, self.config['disk_speed_freq'], volume))
			elif(diskType == "disk_size"):
				for volume in self.config['disk_volumes'].split(','):
					self.list.append(DiskSize(self.arch, self.config['disk_size_freq'], volume))

	def setupNetwork(self, network_types):
		for networkType in network_types:
			if(networkType == "network_errors"):
				for interface in self.config['network_interfaces'].split(','):
					self.list.append(NetworkErrors(self.arch, self.config['network_errors_freq'], interface))
			elif(networkType == "network_drops"):
				for interface in self.config['network_interfaces'].split(','):
					self.list.append(NetworkDrops(self.arch, self.config['network_drops_freq'], interface))
			elif(networkType == "network_bandwidth"):
				for interface in self.config['network_interfaces'].split(','):
					self.list.append(NetworkBandwidth(self.arch, self.config['network_bandwidth_freq'], interface))

	def runCommands(self):
		dataPointObjects = []
		for command in self.list:
			dataPointObjects.extend(command.runCommand())
		for dp in dataPointObjects:
			dp.server_name = self.serverName
		return dataPointObjects
