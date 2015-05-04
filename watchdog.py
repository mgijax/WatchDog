#!/usr/local/bin/python

# Name: watchdog.py
# Purpose: Monitors various server components using a configurable set of
#	scripts that report measurements to this script, which this script
#	then logs to a central Solr server.  This is intended to help us
#	track usage and performance of various server components, with a
#	vision toward helping diagnose (and hopefully predict) problems.
# Usage: See USAGE variable below.

import sys
LIBDIR = '/usr/local/mgi/live/lib/python'
if LIBDIR not in sys.path:
	sys.path.append(LIBDIR)

import os
import time
import getopt
import subprocess
import shlex
import socket
import rcdlib

USAGE = '''Usage: %s [-d] <config file>

    Optional parameters:
    	-d : run in debug mode (no logging to Solr; verbose logging to stdout)

    Required parameters:
	<config file> : specifies the path to the Rcd-formatted file which
		defines the operation of the various measurement scripts
''' % sys.argv[0]

###--- Globals ---###

DEBUG = True			# run in debug mode?
START_TIME = time.time()	# time at which initializion was completed
KEY_FIELD = 'name'		# name of unique key field in config file
DEFAULT_FREQUENCY = None	# default number of seconds between runs of
				# ...each measurement script
RESOLUTION = 0.05		# check processes for completion every
				# ...'RESOLUTION' seconds
MAX_WAIT = 60			# max number of seconds to wait for a process
TESTS = []			# list of Test objects, sorted in order of
				# ...next to execute
SERVER = socket.gethostname()	# name of this server

###--- Functions ---###

def timestamp(sec = None):
	# returns 'sec' as a date/time string, where 'sec' is the number of
	# seconds since the epoch.  If 'sec' is None, the current date/time is
	# returned.

	if not sec:
		sec = time.time()
	return time.strftime('%m/%d/%Y %H:%M:%S', time.localtime(sec))

def debug(s):
	# if we are running in debug mode, write 's' to stdout

	if DEBUG:
		print s
	return

def bailout(s, showUsage = True):
	# print 's' as an error message to stderr; show the 'USAGE' statement,
	# if 'showUsage' is True; and, exit this script with a non-zero exit
	# code (indicating an abnormal exit).

	sys.stderr.write('Error: %s\n' % s)
	if showUsage:
		sys.stderr.write(USAGE)
	sys.exit(1)

def byTime(a,b):
	# comparison function, to order two Test objects by next time to
	# execute

	return cmp(a.getTimeOfNextRun(), b.getTimeOfNextRun())

def setupTests(rcdfile):
	# go through the given RcdFile and set up any related global variables

	global DEFAULT_FREQUENCY, TESTS, SERVER

	# identify the default frequency for collecting measurements, if
	# there is one

	try:
		DEFAULT_FREQUENCY = int(rcdfile.getConstant(
			'DEFAULT_FREQUENCY'))
		debug('Set default frequency of %d seconds' % DEFAULT_FREQUENCY)
	except:
		pass

	# walk through and process each measurement script

	for (name, rcd) in rcdfile.items():
		TESTS.append(Test(rcd))
	
	if len(TESTS) < 1:
		bailout('No tests specified in config file')

	TESTS.sort(byTime)
	debug('Instantiated and sorted %d Test objects' % len(TESTS))

	# override the server name, if one is in the config file

	if rcdfile.getConstant('SERVER_NAME'):
		SERVER = rcdfile.getConstant('SERVER_NAME')

	return TESTS

def parseCommandLine():
	# examine the values passed in on the command-line and do any needed
	# setup of global variables

	global DEBUG

	# look for option flags

	try:
		(opts, args) = getopt.getopt(sys.argv[1:], 'd')
	except getopt.GetoptError, value:
		bailout('Unexpected command-line parameters')

	for (option, value) in opts:
		if option == '-d':
			DEBUG = True
			debug('Turned on debug mode')
		else:
			bailout('Unknown command-line flag: %s' % option)

	# look for config file from command-line

	if len(args) < 1:
		bailout('Missing config file on command-line')
	elif len(args) > 1:
		bailout('Too many command-line arguments')
	elif not os.path.exists(args[0]):
		bailout('Cannot find config file: %s' % args[0])

	debug('Found config file: %s' % args[0])

	# parse config file as an rcd file

	try:
		rcdfile = rcdlib.RcdFile(args[0], rcdlib.Rcd, KEY_FIELD)
	except rcdlib.error, value:
		bailout('Error in file %s : %s' % (args[0], value))
	
	debug('Parsed config file with %d records' % len(rcdfile))

	setupTests(rcdfile)
	return

def logMeasurements(measurements):
	# record this set of measurements in Solr (or write to stderr, if we
	# are running in debug mode

	seconds = time.time()
	datetime = timestamp(seconds)

	names = measurements.keys()
	names.sort()

	for name in names:
		if DEBUG:
			debug('%s %s %s %s %s' % (SERVER, seconds, datetime,
				name, measurements[name]))
		else:
			pass
			# log to Solr
	return

def main():
	# main logic of the script
	global TESTS

	parseCommandLine()

	# At this point, we have a list of all Test objects in global TESTS,
	# sorted in order of next one to execute.

	nextTest = TESTS[0]
	nextTime = nextTest.getTimeOfNextRun()

	# shouldn't be an initial wait, but just in case...
	if nextTime > time.time()
		time.sleep(time.time() - nextTime)
				
	while (nextTime <= time.time()):
		measurements = nextTest.run()

		if measurements:
			logMeasurements(measurements)

		# Until the full sort becomes a performance problem, this is
		# simpler.  If there are enough that this becomes a bottleneck
		# then we can pop off the first item (now done) and walk the
		# list until we find where to insert it. -- max of O(n) time.
		# Could even use a binary search and get to O(log n) time,
		# though not likely we'd see enough of a performance boost to
		# merit it.

		TESTS.sort(byTime)

		nextTest = TESTS[0]
		nextTime = nextTest.getTimeOfNextRun()

		delay = nextTime - time.time()
		if delay > 0:
			time.sleep(delay)
				
	# never returns; infinite loop above.  kill the process if you need
	# to exit.
	return

###--- Classes ---###

class Test:
	def __init__ (self, rcd):
		self.name = rcd[KEY_FIELD]
		self.cmd = rcd['command']
		self.description = rcd['description']
		self.frequency = rcd['frequency']
		self.timeOfNextRun = START_TIME
		self.needShell = False

		if rcd['needShell']:
			self.needShell = True

		# the command is required; if we have no command, then we have
		# an error.

		if not self.cmd:
			bailout('no command defined for "%s"' % self.name)

		# if there is no frequency specific to this measurement, then
		# fall back on the default

		if not self.frequency:
			if DEFAULT_FREQUENCY:
				self.frqeuency = DEFAULT_FREQUENCY
			else:
				bailout('no frequency defined for "%s"' % \
					self.name)

		# otherwise, try to grab the frequency specific for this
		# measurement

		else:
			try:
				self.frequency = int(self.frequency)
			except:
				bailout('Non-integer frequency (%s) for (%s)'\
					% (self.frequency, self.name))

		# if we don't have a description for this measurement, just
		# default to it being the command

		if not self.description:
			self.description = cmd

		# do any pre-processing needed for efficiency

		self.shlexCmd = shlex.split(self.cmd)
		self.retries = MAX_WAIT / RESOLUTION
		return



	def getTimeOfNextRun(self):
		# get the time (in seconds) of when the next run should occur
		return self.timeOfNextRun

	def run(self):
		# do a run of this test, and return a dictionary that maps
		# from each measurement name to its value

		measurements = {}

		# execute the command

		p = subprocess.Popen(self.shlexCmd, shell=self.needShell, stdout=subprocess.PIPE)

		exitCode = p.poll()
		ct = 0

		while (exitCode == None) and (ct <= self.retries):
			ct = ct + 1
			time.sleep(RESOLUTION)
			exitCode = p.poll()

		# if the command didn't finish within the allotted time, we
		# need to kill it and give a message

		if ct > self.retries:
			os.system('kill -9 %s' % p.pid)
			debug('Process %s timed out (%s)' % (p.pid, self.name))

		elif exitCode != 0:
			debug('Process failed with non-zero (%s) exit code, name "%s"' % (exitCode, self.name))

		# otherwise, process its output
		else:
			(stdout, stderr) = p.communicate()
			lines = map(lambda x:x.strip(), stdout.split('\n'))

			for line in lines:
				items = line.split()
				measurement = ' '.join(items[:-1])
				value = None
				
				if len(items) >= 2:
					try:
						value = float(items[-1])
					except:
						debug('Non-numeric value (%s) for measurement (%s)' % (items[-1], measurement))

				if value != None:
					measurements[measurement] = value

		# schedule the next run, and provide a debugging message if
		# the delay between runs is too small

		self.timeOfNextRun = self.timeOfNextRun + self.frequency
		if self.timeOfNextRun <= time.time():
			msg = 'Frequency (%d seconds) is too small for "%s" -- overlapping runs'
			debug(msg % (self.frequency, self.name))

		return measurements
	
###--- Main ---###

if __name__ == '__main__':
	main()
