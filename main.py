#!/usr/bin/python

import ConfigParser, os
from linuxdatapointcollector import LinuxDataPointCollector
import time

if __name__ == '__main__':

	config = ConfigParser.ConfigParser()
	config.readfp(open('monitor_setup.config'))
	dictionary = {}

	for section in config.sections():
		dictionary[section] = {}
		for option in config.options(section):
			dictionary[section][option] = config.get(section, option)

	collector = LinuxDataPointCollector(dictionary['config'])
	points = collector.runCommands()
	print points
	points = collector.runCommands()
	print points
	points = collector.runCommands()
	print points
