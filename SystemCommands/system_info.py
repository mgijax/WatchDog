# This class is used to retrieve info about installed software
# on this server
class SystemInfo(Command):

	def __init__(self, arch, freq):
		Command.__info__(self, arch, freq)

	def run(self):
		return


