import re
import commands
from datapoint import *
from command import Command

# This class is used to retrieve the number of users that are
# logged into the system at any one given time.
class SystemUsers(Command):

	def __init__(self, arch, freq):
		Command.__init__(self, arch, freq)

	def run(self):
		if self.debug: print "uptime"
		string = commands.getstatusoutput("uptime")
		m = re.search('(\d+) user', string[1])
		return [DataPoint("System", "Users", "Users", m.group(1))]


