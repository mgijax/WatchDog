import re
import commands
from datapoint import *
from command import Command

# This class is used to retrieve the uptime that the server has
# This is done by running the uptime command and does simple
# parsing to get the uptime in the a format of dd:hh:mm
class SystemUptime(Command):

	def __init__(self, arch, freq):
		Command.__init__(self, arch, freq)

	def run(self):
		if self.debug: print "uptime"
		string = commands.getstatusoutput("uptime")
		m = re.search('(\d+) day[^\d]+(\d+:?\d+)', string[1])
		return [DataPoint("System", "Uptime", "Uptime", m.group(1) + ":" + m.group(2))]


