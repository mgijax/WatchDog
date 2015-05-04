import json,httplib

class RestClient:

	def __init__(self, restserver, restport):
		self.restserver = restserver
		self.restport = restport
		self.baseurl = "/rest"

	def senddatapoint(self, json_string):
		endpoint = "/serverdata"
		connection = httplib.HTTPConnection(self.restserver, self.restport)
		connection.connect()
		connection.request('POST', self.baseurl + endpoint, json.dumps(json.loads(json_string)), {"Content-Type": "application/json"})
		result = connection.getresponse().read()
		return result
