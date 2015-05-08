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

	def runCommand(self):
		timeToRun = self.lastRuntime <= (time.time() - self.freq)
		if timeToRun:
			self.lastRuntime = time.time()
			try:
				return self.run()
			except:
				return []
		else:
			return []

	def run(self):
		raise NotImplementedError()

class DiskSpeed(Command):

	def __init__(self, arch, freq, volume):
		Command.__init__(self, arch, freq)
		self.volume = volume

	def run(self):
		start = time.time()
		commands.getstatusoutput("touch " + self.volume)
		string1 = commands.getstatusoutput("df -Ph " + self.volume + " | tail -1 | awk '{print $1\"->\"$6}'")
		string = commands.getstatusoutput("dd bs=10240 count=10240 if=/dev/zero of=" + self.volume)
		string = commands.getstatusoutput("dd bs=10240 count=10240 if=/dev/zero of=" + self.volume)
		string = commands.getstatusoutput("dd bs=10240 count=10240 if=/dev/zero of=" + self.volume)
		commands.getstatusoutput("rm " + self.volume)
		end = time.time()
		return [DataPoint("Disk", string1[1], "Speed", str(int(300 / (end - start))))]

class DiskSize(Command):

	def __init__(self, arch, freq, volume):
		Command.__init__(self, arch, freq)
		self.volume = volume

	def run(self):
		commands.getstatusoutput("touch " + self.volume)
		string = commands.getstatusoutput("df -Ph " + self.volume + " | tail -1 | awk '{print $1\"->\"$6}'")
		string2 = commands.getstatusoutput("df -Ph " + self.volume + " | tail -1 | awk '{print $2\":\"$3\":\"$4}'")
		commands.getstatusoutput("rm " + self.volume)
		columns = string2[1].split(":")
		return [
			DataPoint("Disk", string[1], "Used", columns[1]),
			DataPoint("Disk", string[1], "Available", columns[2]),
			DataPoint("Disk", string[1], "Total", columns[0])]

class NetworkErrors(Command):

	def __init__(self, arch, freq, interface):
		Command.__init__(self, arch, freq)
		self.interface = interface

	def run(self):
		if self.arch == "linux":
			string0 = commands.getstatusoutput("cat /sys/class/net/" + self.interface + "/statistics/*_errors")
		if self.arch == "solaris":
			string0 = commands.getstatusoutput("kstat -p -c net -n " + self.interface + " | grep err | awk '{print $2}'")

		errors = 0
		for error in string0[1].split("\n"):
			errors += int(error)

		if self.arch == "linux":
			string1 = commands.getstatusoutput("cat /sys/class/net/" + self.interface + "/statistics/*_dropped")
		if self.arch == "solaris":
			string1 = commands.getstatusoutput("kstat -p -c net -n " + self.interface + " | grep drop | awk '{print $2}'")

		drops = 0
		for drop in string1[1].split("\n"):
			drops += int(drop)

		return [
			DataPoint("Network", self.interface, "Errors", errors),
			DataPoint("Network", self.interface, "Drops", drops)
		]

class NetworkBandwidth(Command):

	def __init__(self, arch, freq, interface):
		Command.__init__(self, arch, freq)
		self.interface = interface

	def run(self):
		if self.arch == "linux":
			string0 = commands.getstatusoutput("cat /sys/class/net/" + self.interface + "/statistics/rx_bytes")
			string1 = commands.getstatusoutput("cat /sys/class/net/" + self.interface + "/statistics/tx_bytes")
			string2 = commands.getstatusoutput("cat /sys/class/net/" + self.interface + "/statistics/rx_packets")
			string3 = commands.getstatusoutput("cat /sys/class/net/" + self.interface + "/statistics/tx_packets")

		if self.arch == "solaris":
			string0 = commands.getstatusoutput("kstat -p -c net -n " + self.interface + " -s rbytes64 | awk '{ print $2 }'")
			string1 = commands.getstatusoutput("kstat -p -c net -n " + self.interface + " -s obytes64 | awk '{ print $2 }'")
			string2 = commands.getstatusoutput("kstat -p -c net -n " + self.interface + " -s ipackets64 | awk '{ print $2 }'")
			string3 = commands.getstatusoutput("kstat -p -c net -n " + self.interface + " -s opackets64 | awk '{ print $2 }'")

		return [
			DataPoint("Network", self.interface, "BytesIn", string0[1]),
			DataPoint("Network", self.interface, "BytesOut", string1[1]),
			DataPoint("Network", self.interface, "PacketsIn", string2[1]),
			DataPoint("Network", self.interface, "PacketsOut", string3[1])
		]

class Load(Command):

	def __init__(self, arch, freq):
		Command.__init__(self, arch, freq)

	def run(self):
		string = commands.getstatusoutput("uptime")
		m = re.search('(\d+\.\d+).*(\d+\.\d+).*(\d+\.\d+)', string[1])
		return [
			DataPoint("System", "Load", "1min", m.group(1)),
			DataPoint("System", "Load", "5min", m.group(2)),
			DataPoint("System", "Load", "15min", m.group(3))]

class Uptime(Command):

	def __init__(self, arch, freq):
		Command.__init__(self, arch, freq)

	def run(self):
		string = commands.getstatusoutput("uptime")
		m = re.search('(\d+) day[^\d]+(\d+:?\d+)', string[1])
		return [DataPoint("System", "Uptime", "Uptime", m.group(1) + ":" + m.group(2))]

class Users(Command):

	def __init__(self, arch, freq):
		Command.__init__(self, arch, freq)

	def run(self):
		string = commands.getstatusoutput("uptime")
		m = re.search('(\d+) user', string[1])
		return [DataPoint("System", "Users", "Users", m.group(1))]

class MemoryRam(Command):

	def __init__(self, arch, freq):
		Command.__init__(self, arch, freq)

	def run(self):
		if self.arch == "linux":
			string = commands.getstatusoutput("free | tail -2 | head -1 | awk '{ print $3\":\"$4; }'")
			columns = string[1].split(":")
			used = columns[0]
			free = columns[1]
			total = int(columns[0]) + int(columns[1])
		if self.arch == "solaris":
			string = commands.getstatusoutput("swap -s")
			m = re.search('(\d+)k bytes allocated \+ (\d+)k reserved = (\d+)k used, (\d+)k available', string[1])
			used = int(m.group(3))
			free = int(m.group(4))
			total = used + free

		return [
			DataPoint("Memory", "Ram", "Used", used),
			DataPoint("Memory", "Ram", "Free", free),
			DataPoint("Memory", "Ram", "Total", total)]

class MemorySwap(Command):

	def __init__(self, arch, freq):
		Command.__init__(self, arch, freq)

	def run(self):
		if self.arch == "linux":
			string = commands.getstatusoutput("free | tail -1 | awk '{ print $2\":\"$3\":\"$4; }'")
			columns = string[1].split(":")
			used = columns[1]
			free = columns[2]
			total = int(columns[1]) + int(columns[2])
		if self.arch == "solaris":
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
