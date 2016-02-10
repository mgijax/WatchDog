import commands
from datapoint import *
from command import Command

# This class gets the mount file system from the file
# that is passed in. It takes the Used, Available and
# Total from the file system and returns it as a data
# point that will be sent to the monitoring server.
class DiskSize(Command):

	def __init__(self, arch, freq, volume):
		Command.__init__(self, arch, freq)
		self.volume = volume

	def run(self):
		if self.debug: print "touch " + self.volume
		commands.getstatusoutput("touch " + self.volume)
		if self.debug: print "df -Ph " + self.volume + " | tail -1 | awk '{print $1\"->\"$6}'"
		string = commands.getstatusoutput("df -Ph " + self.volume + " | tail -1 | awk '{print $1\"->\"$6}'")
		if self.debug: print "df -Ph " + self.volume + " | tail -1 | awk '{print $2\":\"$3\":\"$4}'"
		string2 = commands.getstatusoutput("df -Ph " + self.volume + " | tail -1 | awk '{print $2\":\"$3\":\"$4}'")
		if self.debug: print "rm " + self.volume
		commands.getstatusoutput("rm " + self.volume)
		columns = string2[1].split(":")
		return [
			DataPoint("Disk", string[1], "Used", columns[1]),
			DataPoint("Disk", string[1], "Available", columns[2]),
			DataPoint("Disk", string[1], "Total", columns[0])]


