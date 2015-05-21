from datapoint import *
import commands
import time
import re

class Command:
	lastRuntime = 0

	def __init__(self, arch, freq):
		self.arch = arch
		try:
			self.freq = int(freq)
		except:
			self.freq = 60

	def setDebug(self, debug):
		self.debug = debug

	def runCommand(self):
		timeToRun = self.lastRuntime <= (time.time() - self.freq)
		if timeToRun:
			self.lastRuntime = time.time()
			try:
				if self.debug: print "Running " + self.__class__.__name__ + " Command"
				ret = self.run()
				if self.debug: print "Finished running " + self.__class__.__name__ + " Command"
				if self.debug: print
				return ret
			except Exception, e:
				if self.debug: print "Error: " + str(e)
				if self.debug: print "Finished running " + self.__class__.__name__ + " Command"
				if self.debug: print
				return []
		else:
			if self.debug: print self.__class__.__name__ + " is sleeping for " + str(int(60 - (time.time() - self.lastRuntime))) + " more seconds"
			return []

	def run(self):
		raise NotImplementedError()

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

# This class is used to detect any network error that might
# have occured on a network interface. It tried to determine
# the number of drops and errors per interface card.
class NetworkErrors(Command):

	def __init__(self, arch, freq, interface):
		Command.__init__(self, arch, freq)
		self.interface = interface

	def run(self):
		if self.arch == "linux":
			if self.debug: print "Linux: cat /sys/class/net/" + self.interface + "/statistics/*_errors"
			string0 = commands.getstatusoutput("cat /sys/class/net/" + self.interface + "/statistics/*_errors")
		if self.arch == "solaris":
			if self.debug: print "Solaris: kstat -p -c net -n " + self.interface + " | grep err | awk '{print $2}'"
			string0 = commands.getstatusoutput("kstat -p -c net -n " + self.interface + " | grep err | awk '{print $2}'")

		errors = 0
		for error in string0[1].split("\n"):
			errors += int(error)

		if self.arch == "linux":
			if self.debug: print "Linux: cat /sys/class/net/" + self.interface + "/statistics/*_dropped"
			string1 = commands.getstatusoutput("cat /sys/class/net/" + self.interface + "/statistics/*_dropped")
		if self.arch == "solaris":
			if self.debug: print "Solaris: kstat -p -c net -n " + self.interface + " | grep drop | awk '{print $2}'"
			string1 = commands.getstatusoutput("kstat -p -c net -n " + self.interface + " | grep drop | awk '{print $2}'")

		drops = 0
		for drop in string1[1].split("\n"):
			drops += int(drop)

		return [
			DataPoint("Network", self.interface, "Errors", errors),
			DataPoint("Network", self.interface, "Drops", drops)
		]

# This class is used to get the bandwidth statsistics from a
# network interface. It will grab the number of packets, and
# bytes transmitted and recieved on a interface.
class NetworkBandwidth(Command):

	def __init__(self, arch, freq, interface):
		Command.__init__(self, arch, freq)
		self.interface = interface

	def run(self):
		if self.arch == "linux":
			if self.debug: print "cat /sys/class/net/" + self.interface + "/statistics/rx_bytes"
			string0 = commands.getstatusoutput("cat /sys/class/net/" + self.interface + "/statistics/rx_bytes")
			if self.debug: print "cat /sys/class/net/" + self.interface + "/statistics/tx_bytes"
			string1 = commands.getstatusoutput("cat /sys/class/net/" + self.interface + "/statistics/tx_bytes")
			if self.debug: print "cat /sys/class/net/" + self.interface + "/statistics/rx_packets"
			string2 = commands.getstatusoutput("cat /sys/class/net/" + self.interface + "/statistics/rx_packets")
			if self.debug: print "cat /sys/class/net/" + self.interface + "/statistics/tx_packets"
			string3 = commands.getstatusoutput("cat /sys/class/net/" + self.interface + "/statistics/tx_packets")

		if self.arch == "solaris":
			if self.debug: print "Solaris: kstat -p -c net -n " + self.interface + " -s rbytes64 | awk '{ print $2 }'"
			string0 = commands.getstatusoutput("kstat -p -c net -n " + self.interface + " -s rbytes64 | awk '{ print $2 }'")
			if self.debug: print "Solaris: kstat -p -c net -n " + self.interface + " -s obytes64 | awk '{ print $2 }'"
			string1 = commands.getstatusoutput("kstat -p -c net -n " + self.interface + " -s obytes64 | awk '{ print $2 }'")
			if self.debug: print "Solaris: kstat -p -c net -n " + self.interface + " -s ipackets64 | awk '{ print $2 }'"
			string2 = commands.getstatusoutput("kstat -p -c net -n " + self.interface + " -s ipackets64 | awk '{ print $2 }'")
			if self.debug: print "Solaris: kstat -p -c net -n " + self.interface + " -s opackets64 | awk '{ print $2 }'"
			string3 = commands.getstatusoutput("kstat -p -c net -n " + self.interface + " -s opackets64 | awk '{ print $2 }'")

		return [
			DataPoint("Network", self.interface, "BytesIn", int(string0[1])),
			DataPoint("Network", self.interface, "BytesOut", int(string1[1])),
			DataPoint("Network", self.interface, "PacketsIn", int(string2[1])),
			DataPoint("Network", self.interface, "PacketsOut", int(string3[1]))
		]

# This class is used to retrieve the system load from the
# server. It will return the 1 minute, 5 minute and 15 minute
# load averages that would normally be seen via top or ps
class SystemLoad(Command):

	def __init__(self, arch, freq):
		Command.__init__(self, arch, freq)

	def run(self):
		if self.debug: print "uptime"
		string = commands.getstatusoutput("uptime")
		m = re.search('(\d+\.\d+).*(\d+\.\d+).*(\d+\.\d+)', string[1])
		return [
			DataPoint("System", "Load", "1min", m.group(1)),
			DataPoint("System", "Load", "5min", m.group(2)),
			DataPoint("System", "Load", "15min", m.group(3))]

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

# This class is used to get the amount of free, used, and total
# RAM that a server has. 
class MemoryRam(Command):

	def __init__(self, arch, freq):
		Command.__init__(self, arch, freq)

	def run(self):
		if self.arch == "linux":
			if self.debug: print "Linux: free | tail -2 | head -1 | awk '{ print $3\":\"$4; }'"
			string = commands.getstatusoutput("free | tail -2 | head -1 | awk '{ print $3\":\"$4; }'")
			columns = string[1].split(":")
			used = columns[0]
			free = columns[1]
			total = int(columns[0]) + int(columns[1])
		if self.arch == "solaris":
			if self.debug: print "Solaris: swap -s"
			string = commands.getstatusoutput("swap -s")
			m = re.search('(\d+)k bytes allocated \+ (\d+)k reserved = (\d+)k used, (\d+)k available', string[1])
			used = int(m.group(3))
			free = int(m.group(4))
			total = used + free

		return [
			DataPoint("Memory", "Ram", "Used", used),
			DataPoint("Memory", "Ram", "Free", free),
			DataPoint("Memory", "Ram", "Total", total)]

# This class is used to get the amount of free, used, and total
# Swap space that a server has. 
class MemorySwap(Command):

	def __init__(self, arch, freq):
		Command.__init__(self, arch, freq)

	def run(self):
		if self.arch == "linux":
			if self.debug: print "Linux: free | tail -1 | awk '{ print $2\":\"$3\":\"$4; }'"
			string = commands.getstatusoutput("free | tail -1 | awk '{ print $2\":\"$3\":\"$4; }'")
			columns = string[1].split(":")
			used = columns[1]
			free = columns[2]
			total = int(columns[1]) + int(columns[2])
		if self.arch == "solaris":
			if self.debug: print "Linux: swap -l | tail -1 | awk '{print $4\":\"$5}'"
			string = commands.getstatusoutput("swap -l | tail -1 | awk '{print $4\":\"$5}'")
			columns = string[1].split(":")
			used = int(columns[0]) - int(columns[1])
			free = columns[1]
			total = columns[0]

		return [
			DataPoint("Memory", "Swap", "Used", used),
			DataPoint("Memory", "Swap", "Free", free),
			DataPoint("Memory", "Swap", "Total", total)
		]
