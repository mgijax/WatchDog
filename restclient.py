import httplib

# This class is used to make a connection to the monitoring server
# it will send a json string to a specific endpoint currently hardcoded
# the server will take the data so long as it is well formated and all
# the fields are populated and return a 200
class RestClient:

	def __init__(self, config):
		self.restserver = config['collector_server_name']
		self.restport = config['collector_server_port']
		self.debug = config['debug']
		self.baseurl = "/rest"
		if self.debug: print "Setting up RestClient with url: %s" % "http://" + self.restserver + ":" + self.restport + self.baseurl

	def senddatapoint(self, json_string):
		try:
			endpoint = "/datapoint"
			connection = httplib.HTTPConnection(self.restserver, self.restport)
			connection.connect()
			connection.request('POST', self.baseurl + endpoint, json_string, {"Content-Type": "application/json"})
			result = connection.getresponse().read()
			return result
		except:
			print "Connection to: " + self.restserver + ":" + self.restport + " failed will try again next time"
