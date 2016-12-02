import commands
from datapoint import *
from command import Command

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
		if self.arch == "mac":
			return []

		return [
			DataPoint("Network", self.interface, "BytesIn", int(string0[1])),
			DataPoint("Network", self.interface, "BytesOut", int(string1[1])),
			DataPoint("Network", self.interface, "PacketsIn", int(string2[1])),
			DataPoint("Network", self.interface, "PacketsOut", int(string3[1]))
		]


