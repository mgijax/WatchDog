from systemcommands import *

class DataPointCollector:

	def __init__(self, config):
		self.list = []
		self.serverName = config['server_name']
		self.arch = config['server_arch']
		self.config = config
		self.classobjects = {
			'system_load': Load,
			'system_uptime': Uptime,
			'system_users': Users,
			'memory_ram': MemoryRam,
			'memory_swap': MemorySwap,
			'disk_speed': DiskSpeed,
			'disk_size': DiskSize,
			'network_errors': NetworkErrors,
			'network_bandwidth': NetworkBandwidth
		}
		self.setupCollectionTypes(self.config['collection_types'].split(','))

	def setupCollectionTypes(self, typeList):
		for collectionType in typeList:
			if(collectionType== "system"):
				for systemType in self.config['system_types'].split(','):
					self.list.append(self.classobjects[systemType](self.arch, self.config[systemType + "_freq"]))
			elif(collectionType == "memory"):
				for memoryType in self.config['memory_types'].split(','):
					self.list.append(self.classobjects[memoryType](self.arch, self.config[memoryType + "_freq"]))
			elif(collectionType == "disk"):
				for diskType in self.config['disk_types'].split(','):
					for volume in self.config['disk_volumes'].split(','):
						self.list.append(self.classobjects[diskType](self.arch, self.config[diskType + "_freq"], volume))
			elif(collectionType == "network"):
				for networkType in self.config['network_types'].split(','):
					for interface in self.config['network_interfaces'].split(','):
						self.list.append(self.classobjects[networkType](self.arch, self.config[networkType + "_freq"], interface))
			else:
				print "Unknown Collection Type: %s" % collectionType

	def runCommands(self):
		dataPointObjects = []
		for command in self.list:
			dataPointObjects.extend(command.runCommand())
		for dp in dataPointObjects:
			dp.server_name = self.serverName
		return dataPointObjects
