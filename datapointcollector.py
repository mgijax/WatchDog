from systemcommands import *

# This class reads in the config file and setups all the classes
# that are going to run based on what is found in the config file
# also the config file dictates how often those classes will be
# run. If no entry is found then it just defaults to 60 seconds
class DataPointCollector:

	def __init__(self, config):
		self.list = []
		self.serverName = config['client_name']
		self.arch = config['client_arch']
		self.config = config
		self.debug = config['debug']
		if self.debug: print "Setting up DataPointCollector for: " + self.serverName + " on: " + self.arch
		self.classobjects = {
			'system_load': SystemLoad,
			'system_uptime': SystemUptime,
			'system_users': SystemUsers,
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
					if self.debug: print "Setting up class collector for: %s" % (systemType + " -> " + self.classobjects[systemType].__name__)
					self.list.append(self.classobjects[systemType](self.arch, self.config[systemType + "_freq"]))
			elif(collectionType == "memory"):
				for memoryType in self.config['memory_types'].split(','):
					if self.debug: print "Setting up class collector for: %s" % (memoryType + " -> " + self.classobjects[memoryType].__name__)
					self.list.append(self.classobjects[memoryType](self.arch, self.config[memoryType + "_freq"]))
			elif(collectionType == "disk"):
				for diskType in self.config['disk_types'].split(','):
					for volume in self.config['disk_volumes'].split(','):
						if self.debug: print "Setting up class collector for: %s" % (diskType + " -> " + self.classobjects[diskType].__name__)
						self.list.append(self.classobjects[diskType](self.arch, self.config[diskType + "_freq"], volume))
			elif(collectionType == "network"):
				for networkType in self.config['network_types'].split(','):
					for interface in self.config['network_interfaces'].split(','):
						if self.debug: print "Setting up class collector for: %s" % (networkType + " -> " + self.classobjects[networkType].__name__)
						self.list.append(self.classobjects[networkType](self.arch, self.config[networkType + "_freq"], interface))
			else:
				if self.debug: print "Unknown Collection Type: %s" % collectionType

	def runCommands(self):
		dataPointObjects = []
		for command in self.list:
			command.setDebug(self.debug)
			dataPointObjects.extend(command.runCommand())
		
		if self.debug: print "Collected Data Points: "
		for dp in dataPointObjects:
			dp.server_name = self.serverName
			if self.debug: print dp

		if self.debug: print 
		return dataPointObjects

