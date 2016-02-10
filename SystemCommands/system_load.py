import command as Command

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


