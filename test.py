#!/usr/local/bin/python

from systemcommands.systeminfo import SystemInfo

# This file setups all the collectors
# Then runs all the collectors (commands)
# Then reports all the datapoints to the
# monitoring server. Refer to the github
# page for more information on running
# this client.
if __name__ == '__main__':

	si = SystemInfo("mac", 10)
	si.setDebug(True)
	for dp in si.runCommand():
		dp.server_name = "localhost"
		print dp
