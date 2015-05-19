#!/usr/local/bin/python

import ConfigParser, os
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

	config = ConfigParser.ConfigParser()
	config.readfp(open('host_setup.cfg'))
	dictionary = {}

	for section in config.sections():
		dictionary[section] = {}
		for option in config.options(section):
			dictionary[section][option] = config.get(section, option)

	cfg = dictionary['config']

	restclient = RestClient(cfg)
	collector = DataPointCollector(cfg)

	while True:
		points = collector.runCommands()
		for point in points:
			restclient.senddatapoint(point.json())
		time.sleep(1)
