#!/usr/local/bin/python

import ConfigParser, os, sys
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

	config = ConfigParser.ConfigParser()

	try:
		if debug: print "Loading config file: host_setup.cfg"
		config.readfp(open('host_setup.cfg'))
	except Exception as e:
		if debug: print "Error: Reading config file host_setup.cfg: " + e.strerror
		if debug: print "Consider copying host_setup_default.cfg to host_setup.cfg"
		sys.exit("Error: Config file could not be found")

	dictionary = {}

	for section in config.sections():
		dictionary[section] = {}
		for option in config.options(section):
			dictionary[section][option] = config.get(section, option)

	if debug: print "Finished loading config file into directory"

	cfg = dictionary['config']

	if not "config" in cfg:
		cfg['debug'] = debug

	if debug:
		cfg['debug'] = debug

	restclient = RestClient(cfg)
	collector = DataPointCollector(cfg)

	while True:
		if debug: print "Running commands: "
		points = collector.runCommands()
		for point in points:
			restclient.senddatapoint(point.json())
		time.sleep(1)
