import os
from datapoint import *
from command import Command

# This class is used to retrieve info about installed software
# on this server
class SystemInfo(Command):

	def __init__(self, arch, freq):
		Command.__init__(self, arch, freq)

	def run(self):
		list = []
		packages = {}
		self.recurse("/usr/local/mgi/live", list)
		for d in list:
			if not os.path.islink(d):
				if self.debug:
					print d
				if os.path.isfile(d + "/CVS/Tag"):
					tagfile = open(d + "/CVS/Tag", "r")
					tag = tagfile.readline()[:-1][1:]
					tagfile.close()
					product = os.path.basename(d).split("-")[0]
					if product not in packages:
						packages[product] = []
					packages[product].append(tag)
				elif os.path.isfile(d + "/.git/HEAD"):
					tagfile = open(d + "/.git/HEAD", "r")
					tag = os.path.basename(tagfile.readline()[:-1])
					tagfile.close()
					product = os.path.basename(d)
					if product not in packages:
						packages[product] = []
					packages[product].append(tag)
				else:
					name = os.path.basename(d).split("-")
					product = name[0]
					if len(name) > 1:
						tag = name[1]
					else:
						tag = "trunk"	

					if product not in packages:
						packages[product] = []
					packages[product].append(tag)
				if self.debug:
					print product + " -- " + tag

		return [
			DataPoint("System", "Info", "Packages", packages)
		]

	def recurse(self, dir, list):

		dirs = os.listdir(dir)
		if "CVS" in dirs:
			list.append(dir)
		elif ".git" in dirs:
			list.append(dir)
		else:
			for d in dirs:
				newpath = dir + "/" + d
				if os.path.isdir(newpath):
					self.recurse(newpath, list)

