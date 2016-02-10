import time
import commands
from datapoint import *
from command import Command

# This class is used to write data to disk
# It writes 3 2M files to the file system
# and records the time it takes then does
# the calculation to determine what the
# MB/s would be
class DiskSpeed(Command):

	def __init__(self, arch, freq, volume):
		Command.__init__(self, arch, freq)
		self.volume = volume

	def run(self):
		start = time.time()
		if self.debug: print "touch " + self.volume
		commands.getstatusoutput("touch " + self.volume)
		if self.debug: print "df -Ph " + self.volume + " | tail -1 | awk '{print $1\"->\"$6}'"
		string1 = commands.getstatusoutput("df -Ph " + self.volume + " | tail -1 | awk '{print $1\"->\"$6}'")
		if self.debug: print "dd bs=2048 count=1 if=/dev/zero of=" + self.volume
		string = commands.getstatusoutput("dd bs=2048 count=1 if=/dev/zero of=" + self.volume)
		if self.debug: print "dd bs=2048 count=1 if=/dev/zero of=" + self.volume
		string = commands.getstatusoutput("dd bs=2048 count=1 if=/dev/zero of=" + self.volume)
		if self.debug: print "dd bs=2048 count=1 if=/dev/zero of=" + self.volume
		string = commands.getstatusoutput("dd bs=2048 count=1 if=/dev/zero of=" + self.volume)
		if self.debug: print "rm " + self.volume
		commands.getstatusoutput("rm " + self.volume)
		end = time.time()
		return [DataPoint("Disk", string1[1], "Speed", str(int(6 / (end - start))))]


