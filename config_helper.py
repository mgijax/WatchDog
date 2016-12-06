import ConfigParser, os, sys

class ConfigHelper:

	def __init__(self, debug):

		config = ConfigParser.ConfigParser()

		try:
			if debug: print "Loading config file: host_setup.cfg"
			config.readfp(open('host_setup.cfg'))
		except Exception, e:
			if debug: print "Error: Reading config file host_setup.cfg: " + e.strerror
			if debug: print "Consider copying host_setup_default.cfg to host_setup.cfg"
			sys.exit("Error: Config file could not be found")

		dictionary = {}

		for section in config.sections():
			dictionary[section] = {}
			for option in config.options(section):
				dictionary[section][option] = config.get(section, option)

		if debug: print "Finished loading config file into directory"

		self.cfg = dictionary['config']

		if "debug" not in self.cfg:
			self.cfg['debug'] = debug

		if debug:
			self.cfg['debug'] = debug

		self.cfg['debug'] = (self.cfg['debug'] == True or self.cfg['debug'] == "True")

	def setserverconfig(self, serverconfig):
		self.cfg["types"] = serverconfig["types"]

	def getconfig(self):
		return self.cfg
