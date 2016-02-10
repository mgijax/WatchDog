import command

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

