from systemcommands.systemload import SystemLoad
from systemcommands.systemuptime import SystemUptime
from systemcommands.systeminfo import SystemInfo
from systemcommands.systemusers import SystemUsers
from systemcommands.memoryram import MemoryRam
from systemcommands.memoryswap import MemorySwap
from systemcommands.diskspeed import DiskSpeed
from systemcommands.disksize import DiskSize
from systemcommands.networkerrors import NetworkErrors
from systemcommands.networkbandwidth import NetworkBandwidth

# This class reads in the config file and setups all the classes
# that are going to run based on what is found in the config file
# also the config file dictates how often those classes will be
# run. If no entry is found then it just defaults to 60 seconds
class DataPointCollector:

	def __init__(self, config):
		self.list = []
		self.serverName = config['clientname']
		self.arch = config['clientarch']
		self.config = config
		self.debug = bool(config['debug'])

		if self.debug: print "Setting up DataPointCollector for: " + self.serverName + " on: " + self.arch
		self.classobjects = {
			"System": {
				"Load": SystemLoad,
				"Uptime": SystemUptime,
				"Info": SystemInfo,
				"Users": SystemUptime,
			},
			"Memory": {
				"Ram": MemoryRam,
				"Swap": MemorySwap
			},
			"Disk": {
				"Speed": DiskSpeed,
				"Size": DiskSize,
			},
			"Network": {
				"Errors": NetworkErrors,
				"Bandwidth": NetworkBandwidth
			}
		}
		self.setupCollectionTypes(self.config['types'])

	def setupCollectionTypes(self, typeList):
		for collectionType in typeList:
			for collectionName in collectionType["names"]:
				if len(collectionName["properties"]) > 0:
					for collectionProperty in collectionName["properties"]:
						if collectionType["type"] in self.classobjects and collectionName["name"] in self.classobjects[collectionType["type"]]:
							if self.debug: print "Setting up class collector for: %s" % (collectionType["type"] + "[" + collectionName["name"] + "][" + collectionProperty["property"] + "] -> " + self.classobjects[collectionType["type"]][collectionName["name"]].__name__)
							self.list.append(self.classobjects[collectionType["type"]][collectionName["name"]](self.arch, collectionName["frequency"], collectionProperty["property"]))
				else:
					if collectionType["type"] in self.classobjects and collectionName["name"] in self.classobjects[collectionType["type"]]:
						if self.debug: print "Setting up class collector for: %s" % (collectionType["type"] + "[" + collectionName["name"] + "] -> " + self.classobjects[collectionType["type"]][collectionName["name"]].__name__)
						self.list.append(self.classobjects[collectionType["type"]][collectionName["name"]](self.arch, collectionName["frequency"]))

	def runCommands(self):
		dataPointObjects = []
		for command in self.list:
			command.setDebug(self.debug)
			dataPointObjects.extend(command.runCommand())
		
		if self.debug: print "Collected Data Points: "

		for dp in dataPointObjects:
			dp.server_name = self.serverName
			if self.debug: print dp

		if self.debug: print dataPointObjects
		return dataPointObjects
