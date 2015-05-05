#!/usr/bin/python

import ConfigParser, os
from restclient import *
from linuxdatapointcollector import LinuxDataPointCollector
import time

if __name__ == '__main__':

	config = ConfigParser.ConfigParser()
	config.readfp(open('host_setup.cfg'))
	dictionary = {}

	for section in config.sections():
		dictionary[section] = {}
		for option in config.options(section):
			dictionary[section][option] = config.get(section, option)

	cfg = dictionary['config']
	restclient = RestClient(cfg['collector_server_name'], cfg['collector_server_port'])
	collector = LinuxDataPointCollector(cfg)

	while True:
		points = collector.runCommands()
		for point in points:
			print point.json()
			restclient.senddatapoint(point.json())
		time.sleep(1)
