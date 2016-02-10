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
