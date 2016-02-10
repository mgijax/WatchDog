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


