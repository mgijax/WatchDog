#!/usr/local/bin/python

import ConfigParser, os, sys
from config_helper import *
from restclient import *
from datapointcollector import DataPointCollector
import time

# This file setups all the collectors
# Then runs all the collectors (commands)
# Then reports all the datapoints to the
# monitoring server. Refer to the github
# page for more information on running
# this client.
if __name__ == '__main__':

	debug = False

	if len(sys.argv) > 1:
		if sys.argv[1] == '-d':
			debug = True

	confighelper = ConfigHelper(debug)

	restclient = RestClient(confighelper.getconfig())
	confighelper.setserverconfig(restclient.registerserver())
	collector = DataPointCollector(confighelper.getconfig())

	while True:
		if debug: print "Running commands: "
		points = collector.runCommands()
		for point in points:
			restclient.senddatapoint(point.json())
			pass
		time.sleep(1)
