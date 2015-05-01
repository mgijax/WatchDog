#!/usr/bin/python

import ConfigParser, os
from linuxstatscollector import LinuxStatsCollector

config = ConfigParser.ConfigParser()
config.readfp(open('monitor_setup.config'))
dictionary = {}
for section in config.sections():
	dictionary[section] = {}
	for option in config.options(section):
		dictionary[section][option] = config.get(section, option)

if __name__ == '__main__':
	collector = LinuxStatsCollector(dictionary['config'])
	collector.runCommands()
